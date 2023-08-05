from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup


def get_text(element):
    return element.get_text() if element else None


def parse_page(url):
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run Chrome in headless mode (without UI)
    driver = webdriver.Chrome(options=chrome_options)

    driver.get(url)

    soup = BeautifulSoup(driver.page_source, "html.parser")

    try:
        id = get_text(soup.select_one('div.about-ad-info__id span[style*="color:#737d9b"]'))
        link = get_text(soup.select_one('link[rel="canonical"]'))
        update_date = get_text(soup.select_one('div.about-ad-info__date span:contains("Yenilənmə tarixi") + span'))
        create_date = get_text(soup.select_one('div.about-ad-info__date span:contains("Yaradılma vaxtı") + span'))
        price = get_text(soup.select_one('span.price'))
        currency = get_text(soup.select_one('span.currency'))
        user_name = get_text(soup.select_one('span.userName-text'))
        user_status = get_text(soup.select_one('p.LFParagraph.size-14.userStatus'))
        phone_number = [get_text(item) for item in soup.select('.phone-item span')]
        address_description = get_text(soup.select_one('div.description__wrap p span'))
        address = get_text(soup.select_one('div.pro-item.address div.pro-item__title-wrap p'))
        region_addres = get_text(
            soup.select_one('li p.Paragraph.secondary:contains("Rayon:") + a.LinkText.primary-black.extra-small'))
        metro_station = get_text(soup.select_one(
            'li p.Paragraph.secondary:contains("Metro stansiyası:") + a.LinkText.primary-black.extra-small'))
        official_address = get_text(soup.select_one(
            'li p.Paragraph.secondary:contains("İnzibati rayonlar:") + a.LinkText.primary-black.extra-small'))
        impressions = get_text(soup.select_one('span.Caption.primary:contains("Göstərilmə")'))
        show_button = bool(soup.select_one('button.show-button'))
        view_counts = get_text(soup.select_one('span.Caption.primary:nth-of-type(2)'))
        likes = get_text(soup.select('span.Caption.primary:nth-of-type(2)')[1])
        short_description = get_text(soup.select_one('h1.Heading.secondary-small'))
        count_of_rooms = get_text(soup.select_one(
            'li p.Paragraph.secondary:contains("Otaqların sayı:") + a.LinkText.primary-black.extra-small'))
        area_of_flat = get_text(
            soup.select_one('li p.Paragraph.secondary:contains("Sahə (m2):") + p.Paragraph.secondary'))
        area_of_property = get_text(
            soup.select_one('li p.Paragraph.secondary:contains("Torpaq sahəsi (Sot):") + p.Paragraph.secondary'))
        floor = get_text(
            soup.select_one('li p.Paragraph.secondary:contains("Mərtəbələrin sayı:") + p.Paragraph.secondary'))
        repair_type = get_text(soup.select_one('ul.details-page__params li:nth-child(8) a'))
        flat_type = [get_text(item) for item in soup.select(
            'ul.details-page__params li p:contains("Evin şəraiti:") + a.LinkText.primary-black.extra-small')]
        communal_lines = [get_text(item) for item in soup.select('ul.details-page__params li:nth-child(9) a')]

        return {
            "link": link,
            "id": id,
            "update_date": update_date,
            "create_date": create_date,
            "price": price,
            "currency": currency,
            "user_name": user_name,
            "user_status": user_status,
            "phone_number": phone_number,
            "address_description": address_description,
            "address": address,
            "region_addres": region_addres,
            "metro_station": metro_station,
            "official_address": official_address,
            "impressions": impressions,
            "view_counts": view_counts,
            "likes": likes,
            "show_button": show_button,
            "short_description": short_description,
            "count_of_rooms": count_of_rooms,
            "area_of_flat": area_of_flat,
            "area_of_property": area_of_property,
            "floor": floor,
            "repair_type": repair_type,
            "flat_type": flat_type,
            "communal_lines": communal_lines
        }
    except Exception as e:
        # Log the exception or handle it as per your requirement.
        # You can also return an error dictionary if needed.
        print(f"An error occurred while parsing: {str(e)}")
        return {"error": str(e)}
    finally:
        driver.quit()


# Example usage:
if __name__ == "__main__":
    start_url = "https://lalafo.az/baku/ads/binqdi-qs-3-otaqli-90-kv-m-yeni-tmirli-id-102934449"
    data = parse_page(start_url)
    print(data)
