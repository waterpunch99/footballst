# 1단계: Build
FROM gradle:8.4-jdk17 AS build
WORKDIR /build

COPY . .
RUN gradle bootJar --no-daemon

# 2단계: Run
FROM eclipse-temurin:17-jdk
WORKDIR /app

COPY --from=build /build/build/libs/*.jar app.jar

EXPOSE 8080
ENTRYPOINT ["java", "-jar", "app.jar"]
