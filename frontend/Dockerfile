# frontend/Dockerfile
# 1단계: 빌드 (Vite를 사용하여 정적 파일 생성)
FROM node:18-alpine AS build-stage
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

# 2단계: 배포 (Nginx로 가볍게 서빙)
FROM nginx:stable-alpine
# Vite의 기본 빌드 폴더 명칭은 'dist'입니다 (CRA는 build)
COPY --from=build-stage /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]