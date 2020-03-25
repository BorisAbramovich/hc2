from hashcode.output import write_output
from hashcode.input_data import InputData
from basics import read
import os.path


def main():
    path = '<input-path>'
    name = os.path.basename(path)
    sol = Solution.from_text(read(os.path.join(PROJECT_DIR, path)))
    caches_to_videos = sol.run_batches_joseph(batch_size_multiplier=0.02, timeout=11 * 60)
    out_path = os.path.join(PROJECT_DIR, '../outputs', name + '.out')
    with open(out_path, 'w+') as out_stream:
        write_output(out_stream, caches_to_videos)
    # print(sol)


if __name__ == '__main__':
    print('Starting')
    main()
    print('Done')
