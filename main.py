from email.message import EmailMessage
import smtplib
import ssl
import requests
import os

items_to_check = {
  os.environ["FRONTEND_HASH"]: {
    "name": "Frontend",
    "url": "premid.app"
  },
  os.environ["DOCS_HASH"]: {
    "name": "Docs",
    "url": "docs.premid.app"
  },
  os.environ["DL_HASH"]: {
    "name": "Downloads",
    "url": "dl.premid.app"
  },
  os.environ["CDN_HASH"]: {
    "name": "CDN",
    "url": "cdn.rcd.gg"
  },
  os.environ["API_HASH"]: {
    "name": "API",
    "url": "api.premid.app"
  },
  os.environ["PD_HASH"]: {
    "name": "PD",
    "url": "pd.premid.app"
  }
}

def check_url(url: str) -> bool:
  # Request the url, and see if it returns a 500 error
  try:
    r = requests.get(f"https://{url}")
    print("Received response code: %d" % r.status_code)
    return r.status_code < 500
  except Exception as e:
    print(e)
    return False

def send_email(to: str, result: str) -> None:
  # Create the message
  msg = EmailMessage()
  msg.set_content(result)
  msg["Subject"] = result
  msg["From"] = "premid-status-noreply@theusaf.org"
  msg["To"] = f"component+{to}@notifications.statuspage.io"

  # Send the message
  s = smtplib.SMTP("smtp.gmail.com", 587)
  context = ssl.create_default_context()
  s.starttls(context=context)
  s.login(
    os.environ["USERNAME"],
    os.environ["PASSWORD"]
  )
  s.send_message(msg)
  s.quit()

def main():
  # Check each item
  for item in items_to_check:
    print(f"Checking {items_to_check[item]['name']}...")
    if not check_url(items_to_check[item]["url"]):
      print(f"{items_to_check[item]['name']} is down!")
      send_email(item, "DOWN")
    else:
      print(f"{items_to_check[item]['name']} is up!")
      send_email(item, "UP")

if __name__ == "__main__":
  main()
