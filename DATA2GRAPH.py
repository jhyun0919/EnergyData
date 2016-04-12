# -*- coding: utf-8 -*-

from DATA2VEC import *
import matplotlib.pyplot as plt


# 바이너리 파일들을
# 그래프로 그려 RESULT_DIRECTORY에 저장함
def bins2graphs(file_list):
    path = os.path.join(os.getcwd(), RESULT_DIRECTORY, 'graph')

    if not os.path.exists(path):
        os.makedirs(path)
    os.chdir(path)

    for file in file_list:
        print 'vector 2 graph ' + file,
        start_time = time.time()

        x = []
        for line in unpickling(file)['ts']:
            x.append(line[0])
        y = unpickling(file)['value']

        plt.scatter(x, y, marker='x')

        file_name = file.rsplit('/', 1)[1]

        file_name = file_name.split('.')[0] + '.jpg'

        plt.savefig(file_name)
        plt.close()

        end_time = time.time()
        print '\t\t' + 'run time: ' + str(end_time - start_time)


if __name__ == "__main__":
    start_time = time.time()

    dir_name = get_directory()

    file_list = load_file(dir_name)

    bins2graphs(file_list)

    end_time = time.time()

    print '*** TOATL TIME: ' + str(end_time - start_time) + ' ***'
