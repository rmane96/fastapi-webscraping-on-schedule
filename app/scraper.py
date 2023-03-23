from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver
from fake_useragent import UserAgent
from dataclasses import dataclass
import time


def get_user_agent():
    return UserAgent(verify_ssl=False).random


@dataclass
class Scraper:
    url: str
    endless_scroll :bool = False
    endless_scroll_time : int = 5
    driver: WebDriver = None
    
    def get_driver(self):
        
        if self.driver is None:    
            user_agent = get_user_agent()
            options = Options()
            options.add_argument("--headless")
            options.add_argument("--no-sandbox")
            options.add_argument(f"user-agent={user_agent}")
            driver = webdriver.Chrome(options=options)
            self.driver = driver
        return self.driver
    
    
    def perform_endless_scroll(self,driver):
        if self.endless_scroll:
            current_height = driver.execute_script(
                "return document.body.scrollHeight"
            )
            while True:
                driver.execute_script(
                    "window.scrollTo(0, document.body.scrollHeight)"
                )
                time.sleep(self.endless_scroll_time)
                
                iteration_height = driver.execute_script(
                "return document.body.scrollHeight"
                )
                if current_height == iteration_height:
                    break
                current_height = iteration_height
        return
                
                
    def get(self):
        driver = self.get_driver()
        driver.get(self.url)
        self.perform_endless_scroll(driver=driver)
        
        return driver.page_source
                
        