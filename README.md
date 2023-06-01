# Tag-counter-for-datasets
이미지 태그 데이터셋에서 사용되는 csv 태그 테이터에서 태그가 등장하는 횟수를 세는 프로그램

## 요구사항
- 파이썬
- Pandas 모듈

## 사용법
코드를 다운 받은 후, 같은 폴더에 있는 bat 파일 코드의 옵션 수정 후 bat 파일 실행
### 예시
```
python counting_tags.py --dir="C:\Users\dir\folder" --verbose --extension=caption --output="C:" --recursive
```
## 옵션
--dir 파일을 읽을 경로 입력 (필수)

--verbose 파일명과 태그 내용 출력

--extension 기본값으로 txt 파일을 읽지만, extension 옵션으로 다른 확장자로 변경 가능

--recursive 파일 경로의 하위 폴더도 포함하여 카운팅

--output 태그 카운팅 후, csv 파일을 저장할 경로 지정(지정 안할 경우 dir 폴더에 저장)

--processes 병렬 프로세스로 카운팅

## 병렬 프로세싱 최적화 적용됨

r5-5600u 프로세서로 184,896개의 파일에서 태그 카운팅 76.347 sec 소요됨

![image](https://user-images.githubusercontent.com/14136511/227281258-a05f1b69-0f41-4624-989b-f6fd7a2bffc5.png)
