import pygame
import sys
import random

# Pygame 초기화
pygame.init()
pygame.mixer.init()  # 오디오 믹서 초기화
# 소리 로드
enemy_hit_sound = pygame.mixer.Sound("hit-sound.wav")  # 적 처치 효과음
enemy_hit_sound.set_volume(0.5)  # 볼륨을 50%로 설정
 
# 맵 크기 설정
MAP_WIDTH, MAP_HEIGHT = 5000, 5000  

# 화면 크기 설정
SCREEN_WIDTH, SCREEN_HEIGHT = 1600, 900  # 게임 화면의 가로, 세로 크기
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # 화면 생성
pygame.display.set_caption("도시짱 길냥이")  # 창 제목

MINIMAP_WIDTH, MINIMAP_HEIGHT = 200, 200  # 미니맵 크기
MINIMAP_X, MINIMAP_Y = SCREEN_WIDTH - MINIMAP_WIDTH - 20, 20  # 미니맵 위치 (오른쪽 위)
MINIMAP_SCALE = MINIMAP_WIDTH / MAP_WIDTH  # 미니맵 축소 비율

# 미니맵 크기 및 위치 설정
MINIMAP_WIDTH, MINIMAP_HEIGHT = 200, 200  # 미니맵 크기
MINIMAP_X, MINIMAP_Y = SCREEN_WIDTH - MINIMAP_WIDTH - 20, 20  # 미니맵 위치 (오른쪽 위)
MINIMAP_SCALE = MINIMAP_WIDTH / MAP_WIDTH  # 미니맵 축소 비율

# 미니맵 색상
MINIMAP_BG_COLOR = (200, 200, 200)  # 미니맵 배경 색상
MINIMAP_PLAYER_COLOR = (0, 255, 0)  # 플레이어 색상 (녹색 점)
MINIMAP_ENEMY_COLOR = (255, 0, 0)  # 적 색상 (빨간 점)  

# 한글 폰트 설정
font_path = '온글잎 박다현체.ttf'  # 폰트 파일 경로
font = pygame.font.Font(font_path, 74)
small_font = pygame.font.Font(font_path, 100)  # 점수 표시용 폰트
game_over_font = pygame.font.Font(font_path, 150)  # 게임 오버 텍스트 폰트

# 시작 화면 텍스트
start_text_lines = [
    "도심속 길냥이들의 정점이 되려는냥...",
    "      경쟁자를 냥냥하고 살아남아라!",
    "               [스페이스바]로 냥냥!"
]

# 색상 정의
BLUE = (173, 216, 230)
BLACK = (0, 0, 0)

# 속도 설정
PLAYER_SPEED = 5  # 플레이어 이동 속도
ENEMY_SPEED = 2   # 적 이동 속도
BULLET_SPEED = 20  # 총알 속도

# 이미지 불러오기
player_images = {
    'L_walk': [pygame.image.load('player_L_A.png'), pygame.image.load('player_L_B.png')],  # 왼쪽으로 걷는 애니메이션
    'L_idle': pygame.image.load('player_L_C.png'),  
    'R_walk': [pygame.image.load('player_R_A.png'), pygame.image.load('player_R_B.png')],  # 오른쪽으로 걷는 애니메이션
    'R_idle': pygame.image.load('player_R_C.png'),  
    'L_attack': pygame.image.load('player_L_D.png'),  
    'R_attack': pygame.image.load('player_R_D.png'),  
}

enemy_images = {
    'left': pygame.image.load('enm1.png'),  
    'right': pygame.image.load('enm2.png'),
    'type2_left': pygame.image.load('enm3.png'),
    'type2_right': pygame.image.load('enm4.png')
}

bullet_image = pygame.image.load('bullet_1.png')  
background_image = pygame.image.load('background.png')  

# 이미지 크기 조정
player_size = (150, 150)  
enemy_size = (150, 150)  
bullet_size = (150, 150)  

# 플레이어 이미지를 설정된 크기로 조정
for key in player_images:
    if isinstance(player_images[key], list):  # 리스트(애니메이션 이미지)가 있는 경우
        player_images[key] = [pygame.transform.scale(img, player_size) for img in player_images[key]]
    else:
        player_images[key] = pygame.transform.scale(player_images[key], player_size)

# 적과 총알 이미지를 설정된 크기로 조정
enemy_images['left'] = pygame.transform.scale(enemy_images['left'], enemy_size)
enemy_images['right'] = pygame.transform.scale(enemy_images['right'], enemy_size)
enemy_images['type2_left'] = pygame.transform.scale(enemy_images['type2_left'], enemy_size)
enemy_images['type2_right'] = pygame.transform.scale(enemy_images['type2_right'], enemy_size)
bullet_image = pygame.transform.scale(bullet_image, bullet_size)
background_image = pygame.transform.scale(background_image, (MAP_WIDTH, MAP_HEIGHT))

# 플레이어 초기값
player_x, player_y = 2500, 2500  # 플레이어의 초기 위치
player_facing = 'R'  
player_animation_index = 0  
player_attack_cooldown = 0  # 공격 쿨다운

# 적과 총알의 초기 리스트
enemies = []  # 적을 저장하는 리스트
bullets = []  # 총알을 저장하는 리스트

# 점수 변수 초기화
score = 0

# 맵 위치 (플레이어 위치에 따라 맵 움직임)
map_x, map_y = -player_x + SCREEN_WIDTH // 2, -player_y + SCREEN_HEIGHT // 2

# 게임 루프
clock = pygame.time.Clock()  # 게임의 프레임 속도를 제어하는 Clock 객체를 사용함!!

def draw_minimap():
    # 미니맵 배경 그리기
    pygame.draw.rect(screen, MINIMAP_BG_COLOR, (MINIMAP_X, MINIMAP_Y, MINIMAP_WIDTH, MINIMAP_HEIGHT))

    # 플레이어 위치를 미니맵에 표시
    player_minimap_x = MINIMAP_X + (player_x / MAP_WIDTH) * MINIMAP_WIDTH
    player_minimap_y = MINIMAP_Y + (player_y / MAP_HEIGHT) * MINIMAP_HEIGHT
    pygame.draw.circle(screen, MINIMAP_PLAYER_COLOR, (int(player_minimap_x), int(player_minimap_y)), 5)

    # 적 위치를 미니맵에 표시
    for enemy in enemies:
        enemy_minimap_x = MINIMAP_X + (enemy['x'] / MAP_WIDTH) * MINIMAP_WIDTH
        enemy_minimap_y = MINIMAP_Y + (enemy['y'] / MAP_HEIGHT) * MINIMAP_HEIGHT
        pygame.draw.circle(screen, MINIMAP_ENEMY_COLOR, (int(enemy_minimap_x), int(enemy_minimap_y)), 3)


# 시작 화면 표시 여부
show_start_screen = True  
game_over = False  # 게임 오버 상태

# 메인 게임 루프
while True:
    if show_start_screen:   # 시작 화면
        screen.fill(BLUE)  
        # 텍스트를 각 줄마다 렌더링하여 표시
        y_offset = SCREEN_HEIGHT // 3  # 텍스트 y 위치 설정
        for line in start_text_lines:
            text_surface = font.render(line, True, (0, 0, 0))  # 각 줄을 텍스트로 렌더링
            text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, y_offset))  # 중앙 정렬
            screen.blit(text_surface, text_rect)  # 화면에 텍스트 그리기
            y_offset += 100  # 줄 간격 조정
        

        pygame.display.flip()  # 화면 갱신

        for event in pygame.event.get():  # 이벤트 처리
            if event.type == pygame.QUIT:  # 창을 닫는 이벤트
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:  # 스페이스바 누르면 시작하도록 설정!!
                show_start_screen = False  # 시작 화면 종료
                game_over = False  # 게임 오버 상태 초기화
                score = 0  # 점수 초기화
                player_x, player_y = 2500, 2500  # 플레이어 초기 위치
                enemies.clear()  # 적 초기화
                bullets.clear()  # 총알 초기화
                map_x, map_y = -player_x + SCREEN_WIDTH // 2, -player_y + SCREEN_HEIGHT // 2  # 맵 초기화
    
    elif game_over:  # 게임 오버 화면
        screen.fill(BLUE)
        game_over_text = game_over_font.render("다시 해볼거냥? [ENTER]", True, (0, 0, 0))
        text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))  # 텍스트 중앙 정렬
        screen.blit(game_over_text, text_rect)
        
        # 점수 텍스트 추가
        score_text = small_font.render(f"Score: {score}", True, BLACK)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 150))  # 점수를 게임 오버 텍스트 아래에 배치
        screen.blit(score_text, score_rect)
        pygame.display.flip()

        for event in pygame.event.get():  # 게임 오버 상태에서 이벤트 처리
            if event.type == pygame.QUIT:  # 창을 닫는 이벤트
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:  # Enter 키를 누르면 게임 재시작
                show_start_screen = False  # 시작 화면 종료
                game_over = False  # 게임 오버 상태 초기화
                score = 0  # 점수 초기화
                player_x, player_y = 2500, 2500  # 플레이어 초기 위치
                enemies.clear()  # 적 초기화
                bullets.clear()  # 총알 초기화
                map_x, map_y = -player_x + SCREEN_WIDTH // 2, -player_y + SCREEN_HEIGHT // 2  # 맵 초기화

    else:  # 게임 진행
        screen.fill(BLUE)  
        screen.blit(background_image, (map_x, map_y))  # 배경 이미지

        for event in pygame.event.get():  # 이벤트 처리
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # 마우스 왼쪽 클릭
                if player_attack_cooldown == 0:  # 쿨다운이 0일 때만 총알 생성
                    bullet_direction = pygame.mouse.get_pos()  # 마우스 위치
                    bullet_angle = pygame.math.Vector2(
                        bullet_direction[0] - SCREEN_WIDTH // 2,
                        bullet_direction[1] - SCREEN_HEIGHT // 2
                    ).normalize()  # 총알 방향 계산
                    bullets.append({
                        'x': SCREEN_WIDTH // 2,
                        'y': SCREEN_HEIGHT // 2 - 50,
                        'dx': bullet_angle.x * BULLET_SPEED,
                        'dy': bullet_angle.y * BULLET_SPEED
                    })  
                    player_attack_cooldown = 30  # 공격 쿨다운 설정

        # 메인 게임 루프 안에서
        moving = False  # 이동 여부를 매 프레임마다 초기화
        keys = pygame.key.get_pressed()  # 키 상태 가져오기

        # 플레이어 이동 처리
        keys = pygame.key.get_pressed()
        moving = False

        if keys[pygame.K_w] and player_y > 0:  # 위쪽 경계 확인
            player_y -= PLAYER_SPEED
            moving = True

        if keys[pygame.K_a] and player_x > 0:  # 왼쪽 경계 확인
            player_x -= PLAYER_SPEED
            player_facing = 'L'
            moving = True

        if keys[pygame.K_s] and player_y < MAP_HEIGHT - player_size[1]:  # 아래쪽 경계 확인
            player_y += PLAYER_SPEED
            moving = True

        if keys[pygame.K_d] and player_x < MAP_WIDTH - player_size[0]:  # 오른쪽 경계 확인
            player_x += PLAYER_SPEED
            player_facing = 'R'
            moving = True

        # 벽 충돌 처리 추가
        if player_x < 0:  # 왼쪽 벽 충돌
           player_x = 0
        elif player_x > MAP_WIDTH - player_size[0]:  # 오른쪽 벽 충돌
           player_x = MAP_WIDTH - player_size[0]
    
        if player_y < 0:  # 위쪽 벽 충돌
           player_y = 0
        elif player_y > MAP_HEIGHT - player_size[1]:  # 아래쪽 벽 충돌
           player_y = MAP_HEIGHT - player_size[1]

        # 애니메이션 처리 및 플레이어 그리기
        if moving:
           player_animation_index += 0.1
           current_image = player_images[f'{player_facing}_walk'][int(player_animation_index) % 2]
        else:
           current_image = player_images[f'{player_facing}_idle']

        if player_attack_cooldown > 0:  # 공격 중일 때
           player_attack_cooldown -= 1
           current_image = player_images[f'{player_facing}_attack']

        # 플레이어 그리기
        screen.blit(current_image, (SCREEN_WIDTH // 2 - 75, SCREEN_HEIGHT // 2 - 75))


        # 총알 이동
        for bullet in bullets:
            bullet['x'] += bullet['dx']
            bullet['y'] += bullet['dy']
            screen.blit(bullet_image, (bullet['x'], bullet['y']))

        # 맵을 벗어난 총알 제거
        bullets = [b for b in bullets if 0 <= b['x'] <= SCREEN_WIDTH + 50 and 0 <= b['y'] <= SCREEN_HEIGHT + 50]

        spawn_probability = 2
        if score >= 1000:
            spawn_probability = 4  # 점수 1000 이상일 때 출현 확률 4%
        if score >= 2000:
            spawn_probability = 6  # 점수 2000 이상일 때 출현 확률 6%
        if score >= 3000:
            spawn_probability = 8  # 점수 3000 이상일 때 출현 확률 8%
        if score >= 4000:
            spawn_probability = 10  # 점수 4000 이상일 때 출현 확률 10%
        if score >= 5000:
            spawn_probability = 12  # 점수 5000 이상일 때 출현 확률 12%

        if random.randint(1, 100) <= spawn_probability:
            while True:
                enemy_x = random.randint(0, MAP_WIDTH)
                enemy_y = random.randint(0, MAP_HEIGHT)
                if abs(player_x - enemy_x) >= 900 and abs(player_y - enemy_y) >= 600:
                    # 점수에 따라 적의 타입 결정
                    if score >= 3000:  # 3000점 이상일 때
                        enemy_type = random.choice(['type2_left', 'type2_left', 'left'])  # 새로운 적 등장 확률 높임
                    elif score >= 1500:  # 1500점 이상일 때
                        enemy_type = random.choice(['left', 'type2_left'])  # 기존과 새로운 적 균등 확률
                    else:
                        enemy_type = 'left'  # 기존 적만 생성
                    enemies.append({'x': enemy_x, 'y': enemy_y, 'type': enemy_type})
                    break


        # 적 이동 및 그리기
        for enemy in enemies:
            dx = player_x - enemy['x']
            dy = player_y - enemy['y']
            distance = max(1, (dx ** 2 + dy ** 2) ** 0.5)

            if enemy['type'] == 'left':  # 기존 적
                enemy['x'] += (dx / distance) * ENEMY_SPEED
                enemy['y'] += (dy / distance) * ENEMY_SPEED
            elif enemy['type'] == 'type2_left':  # 새로운 적
                enemy['x'] += (dx / distance) * (ENEMY_SPEED * 1.5)
                enemy['y'] += (dy / distance) * (ENEMY_SPEED * 1.5)

            # 방향과 타입에 따라 적 이미지 선택
            if enemy['type'] == 'left':  # 기존 적
                if enemy['x'] < player_x:
                    enemy_image = enemy_images['right']
                else:
                    enemy_image = enemy_images['left']
            elif enemy['type'] == 'type2_left':  # 새로운 적
                if enemy['x'] < player_x:
                    enemy_image = enemy_images['type2_right']
                else:
                    enemy_image = enemy_images['type2_left']

            screen.blit(enemy_image, (enemy['x'] + map_x, enemy['y'] + map_y))

                # 적과 플레이어 충돌 처리
            if abs(SCREEN_WIDTH // 2 - (enemy['x'] + map_x)) < 75 and abs(SCREEN_HEIGHT // 2 - (enemy['y'] + map_y)) < 75:
                game_over = True  # 게임 오버 상태로 변경
                break

        # 총알과 적의 충돌 처리
        for bullet in bullets[:]:
            for enemy in enemies[:]:
                if abs(bullet['x'] - (enemy['x'] + map_x)) < 75 and abs(bullet['y'] - (enemy['y'] + map_y)) < 75:
                    enemies.remove(enemy)
                    bullets.remove(bullet)
                    enemy_hit_sound.play()  # 적 처치 효과음 재생
                    score += 100  # 점수 증가
                    break

        # 맵 위치 업뎃
        map_x = -player_x + SCREEN_WIDTH // 2
        map_y = -player_y + SCREEN_HEIGHT // 2

        # 점수 표시
        score_surface = small_font.render(f"Score: {score}", True, BLACK)
        screen.blit(score_surface, (50,50))

        draw_minimap()  # 미니맵 그리기
        pygame.display.flip()  # 화면 갱신
        clock.tick(60)  # FPS 설정

pygame.quit()
sys.exit()