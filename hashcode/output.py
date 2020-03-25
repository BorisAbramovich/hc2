from typing import List, Dict


def write_output(out_stream, cache_id_to_videos_ids):
    cache_id_to_videos_ids = {k: v for k, v in cache_id_to_videos_ids.items() if v}
    out_stream.write('{}\n'.format(len(cache_id_to_videos_ids)))
    for cache_id, videos_ids in sorted(cache_id_to_videos_ids.items()):
        out_stream.write(str(cache_id) + ' ')
        out_stream.write(' '.join(str(i) for i in sorted(videos_ids)))
        out_stream.write('\n')
