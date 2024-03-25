from selenium import webdriver
from selenium.webdriver.common.by import By


ALL_PLANS = {'Vivacom': [],
             'A1':[],
             'Yettel': [] 

}



def get_driver(url):
    options = webdriver.ChromeOptions()
    options.add_argument('disable-infobars')
    options.add_argument('start-maximize')
    options.add_argument('disable-dev-shm-usage')
    options.add_argument('no-sandbox')
    options.add_argument('disable-blink-features=AutomationControlled')
    options.add_experimental_option('excludeSwitches', ['enable-automation'])

    driver = webdriver.Chrome(options=options)
    driver.get(url)

    return driver


def get_vivacom_data():

    url = 'https://www.vivacom.bg/online/bg/shop/services/tariff-plan-category-mobile-voice-services/unlimited-max?offer=epc_emj240105094151989465'
    driver = get_driver(url)
    get_all_offers = driver.find_elements(By.CLASS_NAME, "js-related-offer-container")

    for element in get_all_offers:
        plan_data = element.text.splitlines()

        ALL_PLANS['Vivacom'].append({
            'PlanName': plan_data[0],
            'MB': plan_data[3],
            'MaxSpeed': plan_data[4],
            'Minutes': plan_data[1],
            'RoamingMB': plan_data[5],
            'Price': float(plan_data[9].split('лв')[0])
        })
    driver.quit()


def get_a1_data():

    url = 'https://www.a1.bg/a1-one-unlimited'
    driver = get_driver(url)
    driver.set_window_size(1060, 812)

    h2_element = driver.find_element(By.XPATH, "//h2[contains(text(), 'Планове')]")
    next_element = h2_element.find_element(By.XPATH, "following-sibling::div[1]")
    plan_containers = next_element.find_elements(By.XPATH, "*")
    plan_counts = len(plan_containers)

    for i in range(1, plan_counts+1):
        elements = driver.find_elements(By.CSS_SELECTOR, f"div:nth-child({i}) > .rounded-a1 .m-1\\.5")
        for element in elements:
            driver.execute_script("arguments[0].click();", element)

    for index, element in enumerate(next_element.find_elements(By.XPATH, "*")):
        plan_data = element.text.splitlines()
        price = float
        if index == 0:
            price = float(int(plan_data[16])+ 0.01*int(plan_data[17]))
        else:
            price = float(int(plan_data[12])+ 0.01*int(plan_data[13]))
        ALL_PLANS['A1'].append({
            'PlanName': plan_data[0],
            'MB': plan_data[2].split()[0],
            'MaxSpeed': plan_data[3],
            'Minutes': plan_data[1].split()[0],
            'RoamingMB': plan_data[4],
            'Price': price
        })

    driver.quit()


def get_yettel_data():
    url = 'https://shop.yettel.bg/bg/tariff_page'
    driver = get_driver(url)

    plans_container = driver.find_element(By.CLASS_NAME, "tariffs-main-carousel")
    more_info = driver.find_elements(By.CLASS_NAME, "see-more")
    max_speed = str
    minutes = str
    for btn in more_info:
        driver.execute_script("arguments[0].click();", btn)

    for index, element in enumerate(plans_container.find_elements(By.XPATH, "*")):
        plan_data_raw = element.text.splitlines()
        plan_data = [item for item in plan_data_raw if item.strip()]
        price_index = plan_data.index('Виж по-малко') + 1
        if index == len(plans_container.find_elements(By.XPATH, "*"))-1:
            max_speed = plan_data[3]
            minutes = plan_data[4].split()[0]
            roaming_mb = plan_data[13]
        else:
            if index == 1:
                roaming_mb = plan_data[17]
            else:
                roaming_mb = plan_data[15]
            max_speed = plan_data[3] +'. ' + plan_data[4]
            minutes = plan_data[6].split()[0]
            

        ALL_PLANS['Yettel'].append({
            'PlanName': plan_data[0],
            'MB': plan_data[1].split()[0],
            'MaxSpeed': max_speed,
            'Minutes': minutes,
            'RoamingMB': roaming_mb,
            'Price': float(plan_data[price_index].split('лв')[0].replace(',', '.'))
        })

    driver.quit()


if __name__ == "__main__":
    get_vivacom_data()
    get_a1_data()
    get_yettel_data()
    print(ALL_PLANS)