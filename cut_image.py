import random, os, sys, cv2

def cut_image_py(image_name, rows, cols, output_name):

	rows=int(rows)
	cols=int(cols)
 
	# 이미지 파일 경
	image_path = './img/'

	# 이미지 열기
	image = cv2.imread(image_path+f'{image_name}.jpg')

	# 이미지의 크기를 얻음
	height, width, _ = image.shape

	# 이미지가 행과 열로 나눠지지 않을경우, 나머지값을 원본 이미지에서 빼준다
	if height % rows != 0:
		height -= height%rows
	if width % rows != 0:
		width -= width%rows


	# 각 작은 이미지의 크기 계산
	small_height = height // rows
	small_width = width // cols

	# 이미지를 행과 열 개수에 따라 분할하여 저장할 폴더 경로
	output_folder = './cut/'+image_name+'/' 


	# 폴더가 없는 경우 폴더를 생성
	if not os.path.exists(output_folder):
		os.mkdir(output_folder)
        
	# 행과 열이 합만큼 숫자를 리스트로 만듭니다.
	numbers = list(range(rows*cols))

	# 중복 없이 랜덤 숫자 지정
	random_numbers = random.sample(numbers,rows*cols)

	# 이미지를 행과 열 개수에 따라 분할하여 저장
	for i in range(rows):
		for j in range(cols):
			# 이미지를 분할하기 위한 좌표 계산
			y1 = i * small_height
			y2 = (i + 1) * small_height
			x1 = j * small_width
			x2 = (j + 1) * small_width

			# 이미지를 분할하여 저장
			sliced_image = image[y1:y2, x1:x2]
			cv2.imwrite(f'{output_folder}{output_name}_{random_numbers[i*cols+j]}.jpg', sliced_image)


	print('원본 사이즈 : ', image.shape[:2])
	print('수정 사이즈 : ', (height,width))
	print(f'파일명 : {image_name}.jpg')
	print(f'분할 사이즈 : {cols}X{rows}')
	print('이미지 분할 및 저장 완료.')

	return
 

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print('잘못된 인자 개수입니다. image_name rows cols output_name 형식으로 입력해주세요.')
    else:
        image_name=sys.argv[1]
        rows=sys.argv[2]
        cols=sys.argv[3]
        output_name=sys.argv[4]

        output_folder_path = cut_image_py(image_name, rows, cols, output_name)