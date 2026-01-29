# 1. 빌드 스테이지
FROM node:20-slim AS build
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

# 2. 실행 스테이지 (Nginx 사용)
FROM nginx:stable-alpine
# 설정 파일 복사
COPY nginx.conf /etc/nginx/conf.d/default.conf
# 빌드 결과물 복사
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]