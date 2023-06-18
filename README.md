Section3 Project때 다뤘던 Art 2 You모델을 AnimeGAN -> Stable Diffusion 모델로 변경했습니다

runwayml의 레포지토리에서 깃 클론한 파일을 토대로 만들었습니다(https://github.com/runwayml/stable-diffusion)

최종적인 목표는 Stable Diffusion Web-ui같이 사용목적에따라 다양한 모델을 결합한 기능을 구현하는것이며

첫번째 목표 보완점은 ControlNET을 결합하여 원본 이미지를 살리거나 특정 포즈를 설정할수 있는 등의 기능을 사용하는것입니다

현재 오픈소스로 공개되어있는 Stable Diffusion 레포지토리는 일반인이나 사전지식 없는 사람이 사용하기에는 너무 복잡하고 기능이 셀수없이 많아서 쉽게 쓰기에는 무리가 있습니다

이번 프로젝트에서는 prompt, ckpt, strengh 등을 미리 정해놓고 사용자는 간단한 선택만 하면 미리 세팅되어있는 설정대로 변환을 할 수 있게 했습니다

5일이라는 프로젝트 기간동안 flask와 sql관련 보충학습을 하는데에만 해도 시간을 너무 많이 쏟았기때문에 모델의 변환 수행능력은 준수하지 않지만

추후에는 본인의 프로필 사진 변환, 아바타 생성, 그림체 학습 등의 기능을 결합하는 과정을 시간나는대로 조금씩 해볼 예정입니다


로컬에서 이미지 변환시 cuda 메모리부족현상이 일어나서 img2img.py 관련 모든 부분을 cpu로 바꿨습니다

사전학습모델은 https://huggingface.co/dreamlike-art/dreamlike-anime-1.0/resolve/main/dreamlike-anime-1.0.ckpt 을 사용했습니다
