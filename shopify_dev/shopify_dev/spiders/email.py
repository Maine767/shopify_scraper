import scrapy
from time import sleep 
from Logger import Logger

class EmailSpider(scrapy.Spider):
    name = 'Shopify_Emails'
    start_urls = [
    "https://apps.shopify.com/categories/store-management-finances?surface_detail=store-management&surface_inter_position=1&surface_type=category&surface_version=redesign&page=1"
    ]
    db = Logger(dbname="EpsiFund", user="postgres", password="1234", host="localhost", port="5432")


    def number_page(self, url) -> str:

        if url[len(url)-2:].isdigit() == True:
            number = url[len(url)-2:]
        else:
            number = url[len(url)-1:]

        try:
            if self.last_page > 0:
                pass
        except Exception:
            self.last_page = int(number)

        return number
    

    def parse(self, response):
        for link in response.css('div.group-hover\:tw-text-fg-highlight-primary  a::attr(href)'):
            sleep(1)
            yield response.follow(link, callback=self.parse_email)

        pages = response.css("section.tw-block div.tw-flex a::attr(href)").getall()

        try:
            amount_pages = len(pages) - 1
            last_page = pages[amount_pages-1]
            self.number_page(last_page)
        except Exception:
            pass

        try: 
            url = str(response)
            url = url[5:len(url)-1]

            number = self.number_page(url)

            number = int(number) + 1

            if len(str(number)) == 1:
                new_url = url[:len(url)-1] + str(number)
            elif len(str(number)) == 2 and url[len(url)-2:].isdigit() == False:
                new_url = url[:len(url)-1] + str(number)
            else:
                new_url = url[:len(url)-2] + str(number)
        except Exception:
            pass
        
        if number <= self.last_page:
            sleep(1)
            yield response.follow(new_url, callback=self.parse)
        else:
            new_url = ""
            yield response.follow(new_url, callback=self.parse)


    def parse_email(self, response):

        sleep(2)

        info = list()
        email = str()
        avg_rating = str()
        how_many_time_dev = str()
        for i in range(len(response.css('section#adp-developer div.tw-col-span-full p::text'))):
            answer = response.css('section#adp-developer div.tw-col-span-full p::text')[i].get()
            if "@" in answer:
                email = answer
            elif "average rating" in answer:
                avg_rating = answer
            elif "building apps" in answer:
                how_many_time_dev = answer
            else:
                info.append(answer)

        sleep(3)

        try:
            free_trial = response.css('section#adp-pricing div.tw-flex span::text').get()
        except:
            free_trial = "nothing"

        pricing = list()

        try:
            for i in range(len(response.css('section#adp-pricing div.app-details-pricing-plan-card__head'))//2):
                pricing.append(f"{response.css('section#adp-pricing div.app-details-pricing-plan-card__head p::text')[i].get()} – {response.css('section#adp-pricing div.app-details-pricing-plan-card__head h3::text')[i].get()}")
        except:
            pricing = "nothing"

        category = list()
        try:
            for i in range(len(response.css('section#adp-details-section'))):
                category.append(response.css('section#adp-details-section a::text')[i].get())
        except:
            category = "Nothing"


        try:
            launched = response.css('div.tw-mt-4.tw-space-y-6 p::text')[1].get()
        except:
            launched = 'Nothing'

        try:
            language = response.css('div.tw-mt-4.tw-space-y-6 p::text')[3].get()
        except:
            language = 'Nothing'

        try:
            app_rating = response.css('div.tw-pr-md.xl\:tw-pr-lg span::text').get()
        except:
            app_rating = 'Nothing'


        yield {
            'Name': response.css('h1.tw-hyphens::text').get().strip(),
            'Amount_of_apps': response.css('a.lg\:tw-text-body-md::text').get().split()[0],
            'Amount_of_reviews': response.css('section#adp-reviews h2::text').get(),
            'developer': response.css('section#adp-hero div.tw-pl-md.xl\:tw-pl-lg a::text').get().split(),
            'App_rating': app_rating,
            'Launched': launched,
            'Language': language,
            'Info': info,
            'How_many_time_dev': how_many_time_dev,
            'AVG_rating_of_dev_apps': avg_rating,
            'Email': email,
            'Free_trial': free_trial,
            'Pricing': pricing,
            'Category': category
        }
