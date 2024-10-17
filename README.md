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
- 개발환경 : Jupyter notebook, Google Colab(A100)
- DL : Resnet18, YOLOv8(n,s,l)
- 협업 툴 : Slack, Notion
- 디자인 : [Figma](https://www.figma.com/design/VMDwoKV4GzqOgX2aABLjcQ/%ED%8C%8C%EC%9D%B4%EB%84%90%ED%94%84%EB%A1%9C%EC%A0%9D%ED%8A%B8?node-id=1-2&m=dev&t=1NvERl7hZnqNRuDR-1)

## 2. 프로젝트 기간
**전체 기간 : 2024-09-06 ~ 2024-10-07 (1개월)**

## 3. 프로젝트 모델
- Resnet : [Github](링크)
- YOLOv8 : [Github](링크)

## 4. 작업 프로세스
1) 데이터 수집
-	AI Hub 한식 이미지 데이터셋
  * 150종의 한식 이미지(각 종당 약 1,000장) 제공
  * 바운딩 박스 정보 포함
  * [AI Hub 한식 이미지 데이터셋](https://aihub.or.kr/aihubdata/data/view.do?currMenu=115&topMenu=100&aihubDataSe=data&dataSetSn=79)
- 만개의 레시피 데이터
  * 크롤링을 통한 한국 음식 105종의 데이터
  * 번역 API를 이용해 영문 레시피 생성
  * [AI Hub 비전 영역 음식 이미지 데이터셋](https://aihub.or.kr/aihubdata/data/view.do?currMenu=115&topMenu=100&aihubDataSe=data&dataSetSn=71564)
    
2) 데이터 전처리
- 초기에는 AI Hub에서 제공된 바운딩 박스 정보를 활용하여 전처리 없이 YOLOv8n 모델을 학습했으나, 성능이 기대치에 미치지 못함
- 해결 방안
  * roboflow를 사용해 약 10만 장의 이미지를 수동으로 바운딩 박스의 위치를 수정하여 정확도 향상
  * 기존 데이터셋에서 특정 음식 중심으로 불균형이 발생해 데이터 재구성 및 분포 조정

3) 모델 설계 및 학습
- 모델 후보: YOLO-V3, YOLO-V5, YOLO-V8, ResNet 등 다양한 모델 실험
- 하이퍼파라미터 조정: 학습률, 배치 크기, 에폭 수 등을 조정하여 최적 성능 도출
- 학습 프로세스: 데이터셋을 훈련용(80%)과 검증용(20%)으로 분리하고, Loss와 정확도(Accuracy)를 모니터링하며 학습 진행

4) 모델 평가
- 평가지표: mAP, F1-score, Precision-Recall 등의 지표를 사용해 모델 성능 평가
- 혼동 행렬: 모델의 분류 성능을 시각적으로 분석해 문제점 파악

5) 문제점 및 해결방안
- 문제점: ResNet과 YOLO 계열 모델에서 성능 저하 및 객체 인식 실패 문제 발생
- 해결 방안: 데이터 증강, 수동 라벨링을 통한 데이터 품질 개선 및 파라미터 튜닝을 통해 모델 성능 최적화

6) 최종 결과물: 웹서비스 개발
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

1. 홈화면
- 서비스 접속 홈화면으로 검색창을 누르면 이미지 업로드가 가능합니다

| 홈화면 |
|----------|
|![홈화면](https://github.com/your-username/your-repo-name/blob/branch-name/path/to/image.png)|

## 4. 🫶프로젝트 후기

### 😇 김지현
### 😎 강현정
### 🥰 김수명
### 🤩 김예지
### 😘 손민지
### 🥳 한혜승
