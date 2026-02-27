import asyncio
import random
from playwright.async_api import async_playwright, TimeoutError

# ================= CONFIG =================

BASE_URL = "https://demo1.mydayoneai.com/"
PASSWORD = "random_password"

# USERNAMES = ['ace','luffy','sanji','light','usopp','roger'] 

USERNAMES = [
    'sample12@gmail.com',
    'sample33@gmail.com',
    'fedora',
    'sample545@gmail.com',
    'sample35@gmail.com',
    'sample56@gmail.com',
    'sample642@gmail.com',
    'sample123@gmail.com',
    'sample654@gmail.com',
    'sample6w3@gmail.com',
    'jubina@htpl.cc',
    'aslima@htpl.cc',
    'shibil.muhammed@htpl.cc',
    'harsha@htpl.cc',
    'akbar.ali@htpl.cc',
    'shameem.sha@htpl.cc',
    'sona.gopalan@htpl.cc',
    'fidha@htpl.cc',
    'gowtham@htpl.cc',
    'ganesh@htpl.cc',
    'akshay@htpl.cc',
    'adnan@htpl.cc',
    'mohammed.ali@htpl.cc',
    # 'user1@gmail.com',
    # 'user2@gmail.com',
    # 'user3@gmail.com',
    # 'user4@gmail.com',
    # 'user5@gmail.com',
    # 'user6@gmail.com',
    # 'user7@gmail.com',
    # 'user8@gmail.com',
    # 'user9@gmail.com',
    # 'user10@gmail.com',
    # 'user11@gmail.com',
    # 'user143@gmail.com',
    # 'user134@gmail.com',
    # 'user1343@gmail.com',
    # 'user1334@gmail.com',
    # 'user154@gmail.com',
    # 'user16345@gmail.com',
    # 'user176@gmail.com',
    # 'use34rr1@gmail.com',
    # 'use43war1@gmail.com',
    # 'user1gr5@gmail.com',
    # 'usergfrd41@gmail.com',
    # 'user1gr4@gmail.com',
    # 'user1f3@gmail.com',
    # 'user1fer4@gmail.com',
    # 'user1fre4@gmail.com',
    # 'user1erf@gmail.com',
    # 'userefe1@gmail.com',
    # 'user13@gmail.com',
    # 'user14f@gmail.com',
    # 'user5d1@gmail.com',
    # 'user145dfd@gmail.com',
    # 'user164f@gmail.com',
    # 'user153f@gmail.com',
    # 'ankushechopeak@gmail.com',
    # 'bhagyaechopeak@gmail.com',
    # 'echopeakagent1@gmail.com',
    # 'echopeakagent2@gmail.com',
    # 'echopeakagent3@gmail.com',
    # 'echopeakagent4@gmail.com',
    # 'echopeakagent5@gmail.com',
    # 'echopeakagent6@gmail.com',
    # 'echopeakagent7@gmail.com',
    # 'echopeakagent25@gmail.com',
    # 'echopeakagent26@gmail.com',
    # 'echopeakagent30@gmail.com',
    # 'echopeakagent8@gmail.com',
    # 'echopeakagent10@gmail.com',
    # 'echopeakagent11@gmail.com',
    # 'echopeakagent12@gmail.com',
    # 'echopeakagent13@gmail.com',
    # 'echopeakagent14@gmail.com',
    # 'echopeakagent15@gmail.com',
    # 'echopeakagent16@gmail.com',
    # 'echopeakagent17@gmail.com',
    # 'echopeakagent18@gmail.com',
    # 'echopeakagent19@gmail.com',
    # 'echopeakagent20@gmail.com',
    # 'echopeakagent21@gmail.com',
    # 'echopeakagent24@gmail.com',
    # 'echopeakagent29@gmail.com'
]
# Optimized for local machine stability
CONCURRENT_USERS = 20 

# Highly recommended to keep True for 20 users to save RAM/CPU
HEADLESS = True 
NAV_TIMEOUT = 30000
ACTION_TIMEOUT = 10000
ASSESSMENT_MENU_NAME = "My Participation"

failed_users = []
completed_users = []

# =========================================

async def handle_cookie_consent(page):
    try:
        await page.wait_for_selector("text=This application uses cookies", timeout=5000)
        await page.check("input[type='checkbox']")
        await page.click("button:has-text('Ok')")
    except TimeoutError:
        pass  # cookie popup not shown


async def login(page, username):
    await page.goto(BASE_URL, timeout=NAV_TIMEOUT)
    await handle_cookie_consent(page)

    # -------- STEP 1: USERNAME --------
    await page.fill("input[placeholder='Input your Username']", username)
    await page.click("button:has-text('Login'), button:has-text('Next')")
    await page.wait_for_timeout(1000)

    # -------- STEP 2: PASSWORD --------
    await page.fill("input[placeholder='Input your Password']", PASSWORD)
    await page.click("button:has-text('Next')")
    await page.wait_for_load_state("networkidle", timeout=NAV_TIMEOUT)


async def wait_for_spinner(page):
    """Wait for loading spinner to disappear."""
    try:
        spinner = page.locator(".ngx-spinner-overlay")
        if await spinner.is_visible():
            await spinner.wait_for(state="hidden", timeout=5000)
    except:
        pass


async def attempt_assessment(browser, username, semaphore):
    async with semaphore:
        # Increased stagger delay to spread out the CPU load on your machine
        stagger_delay = random.uniform(1.0, 15.0) 
        await asyncio.sleep(stagger_delay)

        context = await browser.new_context(viewport={"width": 1920, "height": 1080})
        page = await context.new_page()
        
        # Abort unnecessary resources to save bandwidth and RAM
        await page.route("**/*.{png,jpg,jpeg,gif,svg,webp,mp4,webm,woff,woff2}", lambda route: route.abort())

        try:
            print(f"🔹 [{username}] Navigating to {BASE_URL}...")
            try:
                await login(page, username)
                print(f"🔹 [{username}] Login successful")
            except Exception as e:
                print(f"❌ [{username}] Login failed: {e}")
                raise e

            # ---------- NEW PROD NAVIGATION ----------
            await page.wait_for_timeout(2500)

            print(f"🔹 [{username}] Expanding 'My Readiness Journey'...")
            await page.locator("text=My Readiness Journey >> visible=true").first.click(timeout=ACTION_TIMEOUT)
            await page.wait_for_timeout(1000) # Wait for accordion to toggle

            print(f"🔹 [{username}] Clicking 'S5-Self Assessment'...")
            await page.locator("text=S5-Self Assessment >> visible=true").first.click(timeout=ACTION_TIMEOUT)
            await page.wait_for_timeout(1000) # Wait for next toggle/menu

            print(f"🔹 [{username}] Clicking '{ASSESSMENT_MENU_NAME}'...")
            await page.locator(f"text={ASSESSMENT_MENU_NAME} >> visible=true").first.click(timeout=ACTION_TIMEOUT)

            print(f"🔹 [{username}] Clicking 'View'...")
            view_button_selector = "button:has-text('View')"
            try:
                await page.wait_for_selector(view_button_selector, timeout=ACTION_TIMEOUT)
                await page.locator(view_button_selector).first.click(timeout=ACTION_TIMEOUT)
            except Exception as e:
                print(f"⚠️ [{username}] Could not click 'View': {e}")
                raise e

            # ---------- CHECK STATUS ----------
            print(f"🔹 [{username}] Checking status...")
            try:
                completed_btn = await page.wait_for_selector("button:has-text('Completed')", timeout=3000)
                is_disabled = await completed_btn.is_disabled()
                if is_disabled:
                    print(f"✅ ALREADY COMPLETED: {username}")
                    completed_users.append(username)
                    return
            except Exception:
                pass 

            # ---------- START ASSESSMENT ----------
            print(f"🔹 [{username}] Clicking 'Attempt' / 'Self Assessment' / 'Continue Attempt'...")
            
            # 1. Reverted to has-text for flexibility. 
            # Note: "has-text('Attempt')" will successfully match BOTH "Attempt" and "Continue Attempt"!
            attempt_btn = page.locator(
                "button:has-text('Attempt'), "
                "button:has-text('Self Assessment')"
            ).first
            
            await attempt_btn.wait_for(state="visible", timeout=ACTION_TIMEOUT)
            await attempt_btn.click(force=True)

            # Add a short pause to allow the screen transition from the Survey Activities to Instructions
            await page.wait_for_timeout(1500)

            print(f"🔹 [{username}] Clicking 'Continue' on Instructions screen...")
            
            # 2. Look for "Continue", but explicitly exclude anything with "Attempt" to avoid old buttons
            continue_btn = page.locator("button:has-text('Continue')").filter(has_not_text="Attempt").first
            await continue_btn.wait_for(state="visible", timeout=ACTION_TIMEOUT)
            await continue_btn.click(force=True)
            
            print(f"🔹 [{username}] Handling initial Modals...")
            try:
                 await page.locator("button:has-text('Ok')").first.click(timeout=3000)
            except:
                 pass

            print(f"🔹 [{username}] Starting Questions Loop...")
            question_count = 1
            
            while True:
                await wait_for_spinner(page)
                try:
                    await page.wait_for_selector("button:has-text('Next'), button:has-text('Submit Answer'), button:has-text('Submit')", timeout=ACTION_TIMEOUT)
                except TimeoutError:
                    print(f"❌ [{username}] Server too slow! Question {question_count} failed to load.")
                    break
                    
                is_answered = False
                textarea = page.locator("textarea")
                
                if await textarea.count() > 0 and await textarea.first.is_visible():
                    current_text = await textarea.first.input_value()
                    if current_text and current_text.strip() != "":
                        print(f"🔹 [{username}] Q{question_count} already has text. Skipping input.")
                        is_answered = True
                    else:
                        print(f"🔹 [{username}] Typing text for Q{question_count}...")
                        await textarea.first.press_sequentially("Automated RPA Response text.", delay=random.randint(30, 80))
                        is_answered = True
                else:
                    input_selector = "input[type='checkbox'], input[type='radio']"
                    click_selector = ".ant-checkbox, input[type='checkbox'], input[type='radio'], [class*='checkbox']"
                    try:
                        await page.wait_for_selector(click_selector, timeout=5000)
                        
                        inputs = await page.query_selector_all(input_selector)
                        for inp in inputs:
                            if await inp.is_checked():
                                print(f"🔹 [{username}] Q{question_count} already selected. Skipping input.")
                                is_answered = True
                                break
                        
                        if not is_answered:
                            think_ms = random.randint(500, 1500)
                            await page.wait_for_timeout(think_ms)
                            
                            options_locator = page.locator(click_selector)
                            options_count = await options_locator.count()
                            
                            if options_count > 0:
                                random_choice = random.randint(0, options_count - 1)
                                
                                await options_locator.nth(random_choice).click(delay=random.randint(50, 150))
                                
                                await page.wait_for_timeout(random.randint(800, 2000))
                                
                                print(f"🔹 [{username}] Selected random option {random_choice + 1} out of {options_count} for Q{question_count}...")
                            else:
                                print(f"⚠️ [{username}] No clickable options found for Q{question_count}!")
                    except Exception as e:
                        print(f"⚠️ [{username}] Could not process options for Q{question_count}: {e}")

                await wait_for_spinner(page)
                submit_btn = page.locator("button:has-text('Submit Answer'), button:has-text('Submit')").first
                next_btn = page.locator("button:has-text('Next')")

                if await submit_btn.is_visible():
                    print(f"🔹 [{username}] Last Question Reached. Waiting for Submit to activate...")
                    
                    await page.wait_for_timeout(2000)
                    
                    retries = 5
                    while retries > 0:
                        if not await submit_btn.is_disabled():
                            break
                        await page.wait_for_timeout(1000)
                        retries -= 1
                    
                    print(f"🔹 [{username}] Clicking Submit...")
                    await submit_btn.scroll_into_view_if_needed()
                    await submit_btn.click(delay=random.randint(50, 150))
                    
                    print(f"🔹 [{username}] Confirming Submission (Clicking Yes)...")
                    try:
                        yes_btn = page.locator("button:has-text('Yes')").first
                        await yes_btn.wait_for(state="visible", timeout=ACTION_TIMEOUT)
                        await page.wait_for_timeout(1000)
                        await yes_btn.click(delay=random.randint(50, 150))
                    except Exception as e:
                        print(f"🔸 [{username}] Confirmation modal check skipped: {e}")
                    
                    print(f"🔹 [{username}] Waiting for submission to process on the server...")
                    try:
                        await wait_for_spinner(page)
                        await page.wait_for_load_state("networkidle", timeout=15000)
                    except Exception:
                        pass
                    
                    print(f"🔹 [{username}] Waiting for completion screen...")
                    try:
                        await page.wait_for_selector("button:has-text('Back')", state="visible", timeout=15000)
                        back_btn = page.locator("button:has-text('Back')").first
                        if await back_btn.is_visible():
                            print(f"🔹 [{username}] Clicking 'Back'...")
                            await back_btn.click(force=True)
                            await page.wait_for_timeout(3000) 
                    except Exception as e:
                        print(f"⚠️ [{username}] Failed to navigate back after submission: {e}")
                    
                    completed_users.append(username)
                    break

                elif await next_btn.is_visible():
                    print(f"🔹 [{username}] Clicking 'Next'")
                    await next_btn.first.scroll_into_view_if_needed()
                    await next_btn.first.click(delay=random.randint(50, 150))
                    
                    # ----------------------------------------------------------------
                    # NEW LOGIC: Check for the validation modal after clicking "Next"
                    # ----------------------------------------------------------------
                    try:
                        # Wait up to 2 seconds for an error modal to pop up
                        # Adjust 'Ok' / 'OK' / 'Close' based on what your specific modal uses
                        modal_btn = page.locator("button:has-text('Ok'), button:has-text('OK'), button:has-text('Close')").first
                        await modal_btn.wait_for(state="visible", timeout=2000)
                        
                        print(f"⚠️ [{username}] Validation modal detected! Closing and retrying Q{question_count}...")
                        await modal_btn.click(delay=random.randint(50, 150))
                        await page.wait_for_timeout(1000) # Give the modal time to disappear
                        
                        # Loop back to the start of the while loop to retry selecting the option 
                        # WITHOUT incrementing question_count
                        continue 
                        
                    except TimeoutError:
                        # If a TimeoutError happens here, it means the modal DID NOT appear. 
                        # That's good! It means "Next" was successful.
                        pass
                    # ----------------------------------------------------------------

                    question_count += 1
                    await page.wait_for_timeout(1000) 
                else:
                    print(f"❌ [{username}] Navigation buttons disappeared. Breaking loop.")
                    break

            print(f"✅ SUCCESS: {username}")

        except TimeoutError:
            print(f"⛔ TIMEOUT: {username}")
            if page:
                try:
                    await page.screenshot(path=f"debug_timeout_{username}.png")
                except: pass
            failed_users.append(username)

        except Exception as e:
            print(f"⛔ ERROR ({username}): {e}")
            if page:
                try:
                    await page.screenshot(path=f"debug_error_{username}.png")
                except: pass
            failed_users.append(username)

        finally:
            if context:
                await context.close()


async def run_load_test():
    semaphore = asyncio.Semaphore(CONCURRENT_USERS)
    
    async with async_playwright() as playwright:
        # Added extra arguments to prevent memory bloat
        browser = await playwright.chromium.launch(
            headless=HEADLESS, 
            args=[
                '--disable-dev-shm-usage',
                '--disable-gpu',
                '--no-sandbox',
                '--disable-extensions'
            ]
        )
        
        # Pulling up to 20 users from the PROD list
        tasks = [attempt_assessment(browser, u, semaphore) for u in USERNAMES[:CONCURRENT_USERS]]
        await asyncio.gather(*tasks)
        
        await browser.close()

        print("\n========= FAILED USERS =========")
        for u in failed_users:
            print(u)

        print("\n========= COMPLETED USERS =========")
        for u in completed_users:
            print(u)


if __name__ == "__main__":
    asyncio.run(run_load_test())