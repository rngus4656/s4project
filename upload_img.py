from PIL import Image

def process_image(input_path='img/input/upload_img.jpg', output_path='img/input/input.jpg', output_size=512):
    # 이미지 열기
    img = Image.open(input_path)

    # 이미지의 가로, 세로 중 더 작은 값으로 정방형 이미지의 크기 결정
    min_length = min(img.size)

    # 이미지의 중앙을 기준으로 정방형 영역 계산
    left = (img.width - min_length) / 2
    top = (img.height - min_length) / 2
    right = (img.width + min_length) / 2
    bottom = (img.height + min_length) / 2

    # 정방형 이미지로 크롭
    img_cropped = img.crop((left, top, right, bottom))

    # 크롭된 이미지가 512x512보다 크거나 작으면 해당 크기로 리사이징
    if max(img_cropped.size) != output_size:
        img_cropped = img_cropped.resize((output_size, output_size), Image.ANTIALIAS)

    # 결과 이미지를 output_path에 저장
    img_cropped.save(output_path)

    return img_cropped

if __name__ == "__main__":
    # 스크립트로 실행될 때만 process_image 함수를 호출
    process_image()
