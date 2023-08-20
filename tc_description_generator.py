import tkinter as tk
from tkinter import scrolledtext
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import urllib.parse


def copy_to_clipboard():
    description = generated_description_text.get("1.0", tk.END)
    app.clipboard_clear()
    app.clipboard_append(description)
    app.update()


def scrape_and_generate_description():
    soundcloud_url = url_entry.get()

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        # Extract artist social links
        artist_page_url = soundcloud_url.split("/")[3]
        artist_url = f"https://soundcloud.com/{artist_page_url}"
        page.goto(artist_url)
        page.wait_for_selector(".web-profiles")
        artist_social_links_html = page.inner_html(".web-profiles")

        # Extract track title
        track_page_url = soundcloud_url
        page.goto(track_page_url)
        page.wait_for_selector(".soundTitle__usernameTitleContainer")
        track_info_html = page.inner_html(".soundTitle__usernameTitleContainer")

        browser.close()

        soup = BeautifulSoup(artist_social_links_html, "html.parser")
        social_links = soup.find_all("a", class_="web-profile")

        track_soup = BeautifulSoup(track_info_html, "html.parser")
        track_title = track_soup.find("h1", class_="soundTitle__title").text.strip()
        artist_name = track_soup.find("h2", class_="soundTitle__username").text.strip()

        generated_description_text.delete("1.0", tk.END)

        description = f"🔥 {track_title} 🔥\n"
        description += f"SoundCloud: {soundcloud_url}\n\n"

        # Trap Cosmos links
        description += "👌 Trap Cosmos 👌\n"
        description += "Discord: https://discord.gg/3gkPHKy\n"
        description += "Instagram: https://www.instagram.com/TrapCosmos\n"
        description += "Twitter: https://twitter.com/TrapCosmos\n"
        description += "SoundCloud: https://soundcloud.com/TrapCosmos\n\n"

        description += f"👌 {artist_name} 👌\n"

        # Artist social links
        for link in social_links:
            link_text = link.text.strip()
            link_href = link.get("href")

            # Exclude email and mailto links
            if not link_href.startswith("mailto"):
                # Remove gate.sc parameters from the link
                clean_link = link_href.split("https://gate.sc?url=")[-1]

                # Replace URL-encoded characters
                clean_link = (
                    urllib.parse.unquote(clean_link)
                    .replace("%2F", "/")
                    .replace("%3A", ":")
                )

                # Remove token at the end of the link
                clean_link = clean_link.split("&token=")[0]

                description += f"{link_text}: {clean_link}\n"

        # Add YouTube link if available
        youtube_link = f"https://www.youtube.com/{artist_page_url}"
        description += f"YouTube: @{artist_page_url}\n" if artist_page_url else ""

        description += "\n📷 Background 📷\n"
        description += "⚠️ ADD UNSPLASH BACKGROUND LINK HERE ⚠️\n\n"
        description += "💫 Epilepsy Warning 💫\n"
        description += "The visuals accompanied with the track may trigger seizures to those with photosensitive epilepsy. Please be cautious."

        generated_description_text.insert(tk.END, description)


app = tk.Tk()
app.title("YouTube Description Generator")
app.geometry("1280x800")

url_label = tk.Label(app, text="Enter SoundCloud Track URL:")
url_label.pack(pady=10)

url_entry = tk.Entry(app)
url_entry.pack(pady=5)

generate_button = tk.Button(
    app, text="Generate Description", command=scrape_and_generate_description
)
generate_button.pack(pady=10)

copy_button = tk.Button(app, text="Copy", command=copy_to_clipboard)
copy_button.pack(pady=5)

generated_description_text = scrolledtext.ScrolledText(app, wrap=tk.WORD)
generated_description_text.pack(fill=tk.BOTH, expand=True, pady=10)

app.mainloop()
