# 🍚 K-food AI : 한식이 궁금하다면 사진만 찍으세요!
![initial](https://github.com/user-attachments/assets/d4067f65-f70e-433d-9321-cba797dc4891)

## 프로젝트 소개
- 한식에 대한 정보가 부족한 외국인들이 한식의 이름과 관련 정보를 쉽게 알 수 있도록 하기 위해 **한식 이미지를 인식 가능한 딥러닝 모델 개발**
- 프로젝트 결과 발표 및 웹사이트 시연 영상 : https://youtu.be/lQ9cWHzCPbI?feature=shared 

## 팀원 소개
|**김지현**|**강현정**|**김수명**|**김예지**|**손민지**|**한혜승**|
|:---:|:---:|:---:|:---:|:---:|:---:|
|[@Whitman](https://github.com/Whitmanbeing)|[@heyroha](https://github.com/heyroha)|[@Sumyeong-Kim](https://github.com/Sumyeong-Kim)|[@ye-jee-hub](https://github.com/ye-jee-hub)|[@eenuskam](https://github.com/eenuskam)|[@tmd03](https://github.com/tmd03)|

## 1. 개발환경
- 개발환경 : Jupyter notebook, Google Colab(A100), VScode
- DL : ResNet18,ResNet50, YOLOv8(n,m,l)
- 협업 툴 : Slack, Notion, google-meet, google-drive
- 디자인 : [Figma](https://www.figma.com/design/VMDwoKV4GzqOgX2aABLjcQ/%ED%8C%8C%EC%9D%B4%EB%84%90%ED%94%84%EB%A1%9C%EC%A0%9D%ED%8A%B8?node-id=1-2&m=dev&t=1NvERl7hZnqNRuDR-1)

## 2. 프로젝트 기간
**전체 기간 : 2024-09-06 ~ 2024-10-07 (1개월)**

## 3. 프로젝트 모델
- Resnet : [Github](https://github.com/FnFood/Food_classification/tree/main/YOLOv8)
- YOLOv8 : [Github](https://github.com/FnFood/Food_classification/tree/main/ResNet)

## 4. 작업 프로세스
**1) 데이터 수집**
- AI Hub 한식 이미지 데이터셋  
  * 150종의 한식 이미지(각 종당 약 1,000장) 제공  
  * 바운딩 박스 정보 포함  
  * [AI Hub 한식 이미지 데이터셋](https://aihub.or.kr/aihubdata/data/view.do?currMenu=115&topMenu=100&aihubDataSe=data&dataSetSn=79)
- 만개의 레시피 데이터  
  * 크롤링을 통한 한국 음식 105종의 데이터  
  * 구글번역 API를 이용해 영문 레시피 생성  
  * [만개의레시피](https://www.10000recipe.com)
    
**2) 데이터 전처리**
- 초기에는 AI Hub에서 제공된 바운딩 박스 정보를 활용하여 전처리 없이 YOLOv8n 모델을 학습했으나, 성능이 기대치에 미치지 못함
- 해결 방안
  * roboflow를 사용해 약 10만 장의 이미지를 수동으로 바운딩 박스의 위치를 수정하여 정확도 향상
  * 기존 데이터셋에서 특정 음식 중심으로 불균형이 발생해 데이터 재구성 및 분포 조정

**3) 모델 설계 및 학습**
- 모델 후보: YOLO-V8(객체인식 모델), ResNet(이미지 분류 모델)
- 모델 사용: YOLO-V8
  * YOLOv8-n 모델: 초기 학습 
  * YOLOv8-m 모델: 수동라벨링 후 성능을 개선하기 위해 학습했으나, 객체 인식이 부족
  * YOLOv8-l 모델: 최종적으로 성능이 가장 좋았으며, 이를 웹서비스에 사용 
- 하이퍼파라미터 조정: 학습률, 배치 크기, 에폭 수 등을 조정하여 최적 성능 도출
- 학습 프로세스: 데이터셋을 훈련용(80%)과 검증용(20%)으로 분리하고, Loss와 정확도(Accuracy)를 모니터링하며 학습 진행

**4) YOLO모델 발전과정**
- 데이터셋에 있는 properties파일을 txt파일로 나눠저장(properties_processing.ipynb)
  * yolov8n_props - runs
- properties파일에 비어있는 부분 기본값(이미지 크기)으로 설정(empty_labeling.ipyb의 첫번째 코드)
  * yolov8n_default - runs_backup
- 기본값으로 설정하는 부분에서 id가 0으로 표시되어 empty_labeling.ipynb의 두번째 코드 실행 하여 수정
  * yolov8_adj_id - runs_fin_demo(epoch25), runs_fin(epoch50)
- roboflow로 수동라벨링한 라벨파일 사용
  * yolov8n_roboflow - new_runs
  * yolov8m_roboflow - m_runs
  * yolov8l_roboflow - l_runs, l_runs2(누락된 라벨 수정)

**5) 모델 평가**
- 평가지표: mAP, F1-score, Precision-Recall 등의 지표를 사용해 모델 성능 평가
- 혼동 행렬: 모델의 분류 성능을 시각적으로 분석해 문제점 파악

**6) 문제점 및 해결방안**
- 문제점: ResNet과 YOLO 계열 모델에서 성능 저하 및 객체 인식 실패 문제 발생
- 해결 방안: 데이터 증강, 수동 라벨링을 통한 데이터 품질 개선 및 파라미터 튜닝을 통해 모델 성능 최적화

**7) 최종 결과물: 웹서비스 개발**
- 설명: YOLOv8-large 모델을 사용하여 한식 이미지를 정확하게 인식하고, 인식된 한식 이름과 레시피를 제공하는 웹서비스
- 주요기능
  * 한식 이미지 업로드 및 인식: 사용자가 한식 이미지를 업로드하면, YOLOv8-large 모델이 해당 음식을 인식하여 이름 추출
  * 레시피 출력: 인식된 한식의 이름과 함께 해당 음식의 조리법을 출력하여 사용자에게 레시피 제공
- 확장 및 발전방안
  * 건강 식단 추천
  * 영양 균형 식단 또는 사용자 맞춤형 식단 추천
  * 사용자의 위치를 기반으로 한 맛집 추천

### [웹사이트 기능설명]
**한식 이미지를 업로드하면 인식을 한 후, 레시피를 출력합니다**

1. 서비스 접속
홈 화면에서 검색창을 누르면 이미지 업로드 가능
2. 음식 인식
딥러닝 모델이 개체를 인식하여 음식을 알려줌
3. 레시피 확인
원하는 음식의 레시피를 클릭하면 해당 음식의 한국어/영어 레시피 출력

| 홈화면 | 음식인식 | 레시피출력 |
|--------|----------|-----------|
| <img src="https://github.com/user-attachments/assets/9a7fc301-d19d-48c4-8018-0895c2054821" alt="홈 화면" width="300"/> | <img src="https://github.com/user-attachments/assets/f700ec4d-c60e-4d0e-bc16-ad57537b7613" alt="음식 인식" width="300"/> | <img src="https://github.com/user-attachments/assets/c588b59c-40ef-4773-ad2d-52b5debe59be" alt="레시피 출력" width="300"/> |

## 4. 🫶프로젝트 후기

### 😇 김지현
딥러닝 프로젝트에서 YOLO 모델을 선정해 한국 음식 이미지 분류를 목표로 개발하고 개선해 나가는 과정이 매우 보람 있었습니다. 특히, 데이터 전처리와 모델 변경 등 여러 과정을 통해 개발 방향을 설정하고, 성능 평가 기준을 세워 프로젝트를 체계적으로 진행한 경험이 의미 있었습니다. 끈기 있게 함께 도전해 준 팀원들에게 진심으로 감사드립니다!
### 😎 강현정
이미지 프로젝트는 처음이라 낯설었는데, 하면서 많이 쓰이는 모델도 한번씩 돌려보면서 많이 배울 수 있었습니다. 중간에 포기하려고 할때 팀원분들께서 열심히 잡고 이끌어 주셔서 마무리까지 올 수 있어서 많이 감사드립니다. 다음 프로젝트는 더 성실하고 열심히 참여해 성과 내보고 싶습니다!
### 🥰 김수명
이번 프로젝트를 통해 데이터 전처리의 중요성을 크게 깨달았습니다. 초기에 YOLOv8n 모델로 시작했으나, 성능 문제를 해결하기 위해 데이터 수동 라벨링과 데이터 증강을 적용했습니다. 이후 YOLOv8-m과 l모델을 적용하면서 모델 성능이 점점 향상되는 것을 직접 느꼈습니다.
프로젝트 기간은 짧았지만, 실질적으로 투자한 긴 시간동안 팀원들과 협력해 문제를 해결하며 팀워크를 강화할 수 있었습니다. 이 프로젝트를 통해 많이 성장할 수 있었습니다. 팀원분들 고생 많으셨습니다!😝
### 🤩 김예지
openCV를 처음 사용해보아 새로웠고, 데이터셋의 중요성을 다시한번 느꼈습니다. AI모델을 개발함에 있어 재료가 되는 데이터셋이 얼만큼 정제되고 가공되어야 좋은 모델이 나오는지 깨닫게 해준 프로젝트였습니다. 수동라벨링이 정말 힘들었지만 그만큼 좋은 성과가 나오게 되어 보람된 시간으로 기억되었습니다.
### 😘 손민지
이미지 처리 프로젝트를 진행해보고 싶었는데, 이번 프로젝트를 통해 그 기회를 가질 수 있어서 매우 좋았습니다. 원하는 결과가 처음부터 나오지 않았지만 그것을 해결해 나가는 과정에서 많은 것을 배웠고, 팀원들과 함께 고생한 끝에 최종적으로 목표한 바를 이룰 수 있어 매우 뿌듯했습니다. 
### 🥳 한혜승
제가 딥러닝이 약해서 조금 걱정했는데 이번 파이널 프로젝트를 통해 얻어가는게 많은 것 같습니다. 그리고 이번 프로젝트에서 웹 서비스 디자인을 맡게 되어 새로운 도전도 해보았고, 다같이 밤새 라벨링한 건 정말 기억에 오랫동안 남을 것 같습니다. 팀원분들 너무 감사합니다!😍
