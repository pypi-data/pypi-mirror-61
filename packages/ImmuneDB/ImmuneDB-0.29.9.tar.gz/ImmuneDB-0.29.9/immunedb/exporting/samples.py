from sqlalchemy import func

from immunedb.common.models import CloneStats, Sample, SampleMetadata
from immunedb.exporting.tsv_writer import StreamingTSV
from immunedb.exporting.writer import ExportWriter
from immunedb.util.log import logger


class Passthrough:
    def __getattr__(self, attr):
        return 0


def get_samples(session, for_update=False, sample_ids=None):
    meta = [
        s.key for s in session.query(SampleMetadata.key).group_by(
            SampleMetadata.key).order_by(SampleMetadata.key)
    ]

    clone_cnts = {s.sample_id: s.clones for s in session.query(
        CloneStats.sample_id,
        func.count(CloneStats.clone_id.distinct()).label('clones')
    ).filter(
        ~CloneStats.sample_id.is_(None)
    ).group_by(CloneStats.sample_id)}

    if for_update:
        fields = ['id', 'name', 'subject']
    else:
        fields = ['id', 'name', 'subject', 'input_sequences', 'identified',
                  'in_frame', 'stops', 'functional', 'avg_clone_cdr3_num_nts',
                  'avg_clone_v_identity', 'clones']
    fields.extend(meta)
    writer = StreamingTSV(fields)
    yield writer.writeheader()
    samples = session.query(Sample)
    if sample_ids:
        samples = samples.filter(Sample.id.in_(sample_ids))
    for sample in samples.order_by(Sample.name):
        row = {
            'id': sample.id,
            'name': sample.name,
            'subject': sample.subject.identifier,
        }
        stats = sample.stats if sample.stats else Passthrough()
        if not for_update:
            v_iden = session.query(
                func.avg(CloneStats.avg_v_identity).label('avg')
            ).filter(
                CloneStats.sample_id == sample.id
            ).first()
            cdr3_len = session.query(
                CloneStats
            ).filter(
                CloneStats.sample_id == sample.id
            )
            cdr3_len = [c.clone.cdr3_num_nts for c in cdr3_len]
            if cdr3_len:
                cdr3_len = sum(cdr3_len) / len(cdr3_len)
            else:
                cdr3_len = 'NA'

            row.update({
                'input_sequences': stats.sequence_cnt +
                stats.no_result_cnt,
                'identified': stats.sequence_cnt,
                'in_frame': stats.in_frame_cnt,
                'stops': stats.stop_cnt,
                'avg_clone_v_identity': round(v_iden.avg, 5)
                if v_iden else 'NA',
                'avg_clone_cdr3_num_nts': round(cdr3_len, 5),
                'functional': stats.functional_cnt,
                'clones': clone_cnts.get(sample.id, 0)
            })

        row.update(sample.metadata_dict)
        yield writer.writerow(row)


def write_samples(session, sample_ids=None, for_update=False, zipped=False,
                  **kwargs):
    logger.info('Exporting samples')
    with ExportWriter(zipped) as fh:
        fh.set_filename('samples.tsv')
        fh.write(get_samples(session, for_update, sample_ids))
        return fh.get_zip_value()
