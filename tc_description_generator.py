import tkinter as tk
from tkinter import scrolledtext, messagebox
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import urllib.parse


# Function to copy the generated description to the clipboard
def copy_to_clipboard():
    description = generated_description_text.get("1.0", tk.END)
    app.clipboard_clear()
    app.clipboard_append(description)
    app.update()


# Function to show loading indicator on the generate button
def show_loading_indicator():
    generate_button.config(state=tk.DISABLED)
    generate_button.config(text="Generating...")
    app.update()


# Function to hide loading indicator on the generate button
def hide_loading_indicator():
    generate_button.config(state=tk.NORMAL)
    generate_button.config(text="Generate Description")
    app.update()


# Function to scrape and generate the YouTube description
def scrape_and_generate_description():
    soundcloud_url = url_entry.get()

    # Validate SoundCloud URL
    if not soundcloud_url.startswith("https://soundcloud.com"):
        messagebox.showerror(
            "Invalid URL", "Please enter a valid SoundCloud track URL."
        )
        return

    show_loading_indicator()

    # Use Playwright to extract social links and track info
    with sync_playwright() as p:
        browser = p.chromium.launch()
        artist_page_url = soundcloud_url.split("/")[3]
        artist_url = f"https://soundcloud.com/{artist_page_url}"
        track_page_url = soundcloud_url

        with browser.new_page() as page:
            page.goto(artist_url)
            page.wait_for_selector(".web-profiles")
            artist_social_links_html = page.inner_html(".web-profiles")

            page.goto(track_page_url)
            page.wait_for_selector(".soundTitle__usernameTitleContainer")
            track_info_html = page.inner_html(".soundTitle__usernameTitleContainer")

    # Extract and process artist social links
    soup = BeautifulSoup(artist_social_links_html, "html.parser")
    social_links = soup.find_all("a", class_="web-profile")

    # Extract track title and artist name
    track_soup = BeautifulSoup(track_info_html, "html.parser")
    track_title = track_soup.find("h1", class_="soundTitle__title").text.strip()
    artist_name = track_soup.find("h2", class_="soundTitle__username").text.strip()

    generated_description_text.delete("1.0", tk.END)

    description = f"🔥 {track_title} 🔥\n"
    description += f"SoundCloud: {soundcloud_url}\n\n"

    # Add fixed Trap Cosmos social links
    description += "👌 Trap Cosmos 👌\n"
    description += "Discord: https://discord.gg/3gkPHKy\n"
    description += "Instagram: https://www.instagram.com/TrapCosmos\n"
    description += "Twitter: https://twitter.com/TrapCosmos\n"
    description += "SoundCloud: https://soundcloud.com/TrapCosmos\n\n"

    description += f"👌 {artist_name} 👌\n"

    # Process and add common social links
    for link in social_links:
        link_text = link.text.strip()
        link_href = link.get("href")

        if (
            "instagram" in link_href.lower()
            or "twitter" in link_href.lower()
            or "facebook" in link_href.lower()
            or "soundcloud" in link_href.lower()
            or "youtube" in link_href.lower()
        ):
            clean_link = (
                urllib.parse.unquote(link_href.split("https://gate.sc?url=")[-1])
                .replace("%2F", "/")
                .replace("%3A", ":")
            )
            clean_link = clean_link.split("&token=")[0]

            # Capitalize the link text and remove '.' at the end
            capitalized_link_text = link_text.capitalize().rstrip(".")

            description += f"{capitalized_link_text}: {clean_link}\n"

    description += "\n📷 Background 📷\n"
    description += "⚠️ ADD UNSPLASH BACKGROUND LINK HERE ⚠️\n\n"

    description += "💫 Epilepsy Warning 💫\n"
    description += "The visuals accompanied with the track may trigger seizures to those with photosensitive epilepsy. Please be cautious."

    generated_description_text.insert(tk.END, description)
    hide_loading_indicator()


# Create the main application window
app = tk.Tk()
app.title("YouTube Description Generator")
app.geometry("1280x800")

# Add URL entry and generate button
url_label = tk.Label(app, text="Enter SoundCloud Track URL:")
url_label.pack(pady=10)

url_entry = tk.Entry(app)
url_entry.pack(pady=5)

generate_button = tk.Button(
    app, text="Generate Description", command=scrape_and_generate_description
)
generate_button.pack(pady=10)

clear_button = tk.Button(
    app,
    text="Clear Description",
    command=lambda: generated_description_text.delete("1.0", tk.END),
)
clear_button.pack(pady=5)

copy_button = tk.Button(app, text="Copy to Clipboard", command=copy_to_clipboard)
copy_button.pack(pady=5)

# Add the generated description text area
generated_description_text = scrolledtext.ScrolledText(app, wrap=tk.WORD)
generated_description_text.pack(fill=tk.BOTH, expand=True, pady=10)

# Start the GUI event loop
app.mainloop()
