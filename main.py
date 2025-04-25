from seleniumbase import Driver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def verificar_captcha(driver):
    """Verifica se há CAPTCHA visível na página"""
    try:
        captcha_frames = driver.find_elements(By.XPATH, '//iframe[contains(@src, "captcha") or contains(@title, "CAPTCHA")]')
        if captcha_frames:
            print("⚠️ CAPTCHA detectado - Resolução necessária")
            return True
        
        captcha_elements = driver.find_elements(By.XPATH, '//*[contains(@class, "captcha") or contains(@id, "captcha")]')
        if captcha_elements and any(element.is_displayed() for element in captcha_elements):
            print("⚠️ CAPTCHA detectado - Resolução necessária")
            return True
            
        return False
    except:
        return False

driver = Driver(uc=True, headless=False)
driver.maximize_window()

try:
    print("Acessando Bet365...")
    driver.get("https://www.bet365.com/")
    
    if verificar_captcha(driver):
        print("🛑 Por favor, resolva o CAPTCHA manualmente")
        start_time = time.time()
        while verificar_captcha(driver) and (time.time() - start_time) < 120:
            time.sleep(5)
        print("CAPTCHA resolvido ou timeout atingido")

    try:
        print("Procurando botão de cookies...")
        cookie_buttons = WebDriverWait(driver, 15).until(
            EC.presence_of_all_elements_located((By.XPATH, 
                '//button[contains(@class, "cookie") or contains(@id, "cookie") or contains(text(), "Aceitar") or contains(text(), "Concordar")]'))
        )
        
        for btn in cookie_buttons:
            if btn.is_displayed():
                driver.execute_script("arguments[0].scrollIntoView();", btn)
                driver.execute_script("arguments[0].click();", btn)
                print("✅ Cookies aceitos")
                break
    except Exception as e:
        print(f"⚠️ Não foi possível aceitar cookies: {str(e)[:100]}")

    print("Navegando para Futebol...")
    try:
        try:
            menu_esportes = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, '//div[contains(@class, "sm-SportsMenuButton")]'))
            )
            menu_esportes.click()
            print("✅ Menu de esportes aberto")
        except:
            print("⚠️ Não foi possível abrir o menu de esportes, tentando alternativa...")
        
        futebol_encontrado = False
        tentativas_futebol = [
            '//div[contains(@class, "sm-SportsMenuButton_Label") and (contains(., "Futebol") or contains(., "Futbol"))]',
            '//div[contains(., "Futebol - fim de semana")]',
            '//div[contains(., "Futebol") and not(contains(., "Ao Vivo"))]',
            '//a[contains(@href, "soccer")]',
            '//span[contains(., "Futebol")]'
        ]
        
        for tentativa in tentativas_futebol:
            try:
                elemento_futebol = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, tentativa))
                )
                driver.execute_script("arguments[0].scrollIntoView();", elemento_futebol)
                driver.execute_script("arguments[0].click();", elemento_futebol)
                print(f"✅ Aba de Futebol encontrada via: {tentativa[:50]}...")
                futebol_encontrado = True
                break
            except:
                continue
        
        if not futebol_encontrado:
            raise Exception("Não foi possível encontrar a aba de Futebol após várias tentativas")

        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, '//div[contains(@class, "sm-CouponLink")]'))
        )
        print("✅ Jogos carregados")

    except Exception as e:
        print(f"⚠️ Erro ao navegar para Futebol: {str(e)[:100]}")
        raise

    print("Procurando Internacional x Juventude...")
    try:
        jogo_xpaths = [
            '//div[contains(@class, "sm-CouponLink") and contains(., "Internacional") and contains(., "Juventude")]',
            '//div[contains(@class, "sl-CouponParticipantWithBookCloses") and contains(., "Internacional") and contains(., "Juventude")]',
            '//div[contains(@class, "rcl-ParticipantFixtureDetailsTeam") and contains(., "Internacional")]/../..//div[contains(., "Juventude")]'
        ]
        
        jogo = None
        for xpath in jogo_xpaths:
            try:
                jogo = WebDriverWait(driver, 15).until(
                    EC.presence_of_element_located((By.XPATH, xpath))
                )
                print(f"✅ Jogo encontrado via: {xpath[:50]}...")
                break
            except:
                continue
        
        if not jogo:
            raise Exception("Jogo não encontrado após várias tentativas")
        
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", jogo)
        time.sleep(1)
        
        tentativas_clique = [
            lambda: driver.execute_script("arguments[0].click();", jogo),
            lambda: ActionChains(driver).move_to_element(jogo).pause(1).click().perform(),
            lambda: jogo.click()
        ]
        
        for tentativa in tentativas_clique:
            try:
                tentativa()
                print("✅ Jogo clicado com sucesso")
                break
            except:
                continue
        else:
            raise Exception("Não foi possível clicar no jogo")
        
        time.sleep(3)

        print("Buscando Over 1.5...")
        over_xpaths = [
            '//div[contains(@class, "gl-ParticipantOddsOnly") and contains(., "Over 1.5")]',
            '//div[contains(., "Over") and contains(., "1.5")]',
            '//span[contains(., "Over 1.5")]',
            '//div[contains(@class, "bbl-BetBuilderParticipant") and contains(., "Over 1.5")]'
        ]
        
        for xpath in over_xpaths:
            try:
                odd = WebDriverWait(driver, 15).until(
                    EC.visibility_of_element_located((By.XPATH, xpath))
                )
                print(f"✅ Odd encontrada: {odd.text}")
                break
            except:
                continue
        else:
            print("⚠️ Odd Over 1.5 não encontrada")
                
    except Exception as e:
        print(f"⚠️ Erro ao interagir com o jogo: {str(e)[:100]}")
        raise

except Exception as e:
    print(f"⚠️ Erro fatal: {str(e)[:100]}")
finally:
    input("Pressione Enter para fechar...")
    driver.quit()