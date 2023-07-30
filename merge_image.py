import numpy as np
import random, os, sys, cv2

def merge_image_py(input_name, rows, cols, output_name):
        
    # 이미지를 섞고 퍼즐처럼 배치하는 함수
    def mix_images_into_puzzle(images, grid_size):
        random.shuffle(images)  # 이미지들을 랜덤하게 섞음
        rows, cols = grid_size
        base_height, base_width, _ = images[0].shape
        puzzle_height = base_height * rows
        puzzle_width = base_width * cols
        puzzle_image = np.zeros((puzzle_height, puzzle_width, 3), dtype=np.uint8)

        index = 0
        for i in range(rows):
            for j in range(cols):
                image = images[index]
                puzzle_image[i*base_height:(i+1)*base_height, j*base_width:(j+1)*base_width] = image
                index += 1

        return puzzle_image

    rows=int(rows)
    cols=int(cols)

    # 원본 이미지 경로
    orignal_dir = './img/'+input_name+'.jpg'
    
    # 이미지 디렉토리 경로
    image_dir = './cut/'+input_name

    # 디렉토리에 있는 모든 파일 가져오기
    file_list = os.listdir(image_dir)

    # 이미지들을 리스트로 묶음
    images = []
    for file_name in file_list:
        image_path = os.path.join(image_dir, file_name)
        image = cv2.imread(image_path)
        images.append(image)

    # 원본 이미지를 불러옴 (임의로 설정한 원본 이미지 경로)
    original_image = cv2.imread(orignal_dir,cv2.IMREAD_COLOR)

    # SIFT 디스크립터 추출기 생성
    sift = cv2.SIFT_create()

    # 원본 이미지의 특징점과 디스크립터 추출
    kp, des = sift.detectAndCompute(image, None)
    kp_original, des_original = sift.detectAndCompute(original_image, None)

    # 이미지들의 특징점과 디스크립터 추출
    descriptors = []
    used_images = []  # 이미지 사용 여부를 기록하는 리스트
    for image in images:
        kp, des = sift.detectAndCompute(image, None)
        descriptors.append(des)
        used_images.append(False)  # 모든 이미지를 아직 사용하지 않았다고 표시

    # 이미지를 퍼즐처럼 섞고 하나의 이미지로 만듦
    grid_size = (rows, cols)  # 퍼즐의 행과 열 개수
    puzzle_image = mix_images_into_puzzle(images, grid_size)

    # FlannBasedMatcher 생성
    flann = cv2.FlannBasedMatcher()
    
    # 원본 이미지와 각 이미지 조각들과의 유사도를 평가
    best_order = [0]
    best_similarity = 0
    unused_indices = list(range(1, len(descriptors)))  # 모든 이미지 인덱스를 저장한 리스트

    while len(unused_indices) > 0:
        best_similarity = 0
        best_index = -1

        for j in unused_indices:
            matches = flann.knnMatch(des_original, descriptors[j], k=2)
            good_matches = [m for m, n in matches if m.distance < 0.75* n.distance]
            similarity = len(good_matches)
            if similarity > best_similarity:
                best_similarity = similarity
                best_index = j

        best_order.append(best_index)
        unused_indices.remove(best_index)
        
    # 이미지를 최적의 순서로 배치하여 하나의 이미지로 만듦
    for i in range(len(best_order)):
        image = images[best_order[i]]
        row = i // 2
        col = i % 2
        puzzle_image[row*image.shape[0]:(row+1)*image.shape[0], col*image.shape[1]:(col+1)*image.shape[1]] = image

        
    # 이미지 디렉토리 경로
    merge_dir = './merge/'
    
    # 퍼즐 이미지를 저장
    cv2.imwrite(merge_dir+f'{input_name}_{output_name}_merge.jpg', puzzle_image)

    # 유사도 출력
    print('유사도:', best_similarity)
    print(f'파일명: {input_name}_{output_name}_merge.jpg')

    return


if __name__ == "__main__":
    if len(sys.argv) != 5:
        print('잘못된 인자 개수입니다. input_name rows cols output_name 형식으로 입력해주세요.')
    else:
        input_name=sys.argv[1]
        rows=sys.argv[2]
        cols=sys.argv[3]
        output_name=sys.argv[4]

        output_folder_path = merge_image_py(input_name, rows, cols, output_name)