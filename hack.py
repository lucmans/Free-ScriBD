#!/bin/python3

# TODO:
#   - Download book. Problem is, the book is defined in HTML and CSS and uses files which are stored on a Scribd server.
#       Options:
#         - Try to download all the files, images and fonts. Then use the Javascript from Scribd to view it.
#         - Try to get the "made" pages (ask from DOM?) as image of pdf, or actually find a way to print it (protected by site).
#
#       Tried:
#         - Printing the page. This is prevented by the site.
#         - Only printing the class="document_container" element.
#         - Copying the HTML, CSS and images and view it in a browser.
#
#   - Remove more unneeded elements from the page.
#   - Start in fullscreen.


import sys
from selenium import webdriver


elementsToRemove = ["page_missing_explanation outer_page only_ie6_border between_page_module",
                    "autogen_class_views_pdfs_page_blur_promo autogen_class_widgets_base",
                    "between_page_ads",
                    "buy_doc_bar outer_page only_ie6_border between_page_module",
                    "newpage",  # All the correct pages get loaded from the scribd server. So remove all present pages (the first view which you can view for free).
                    "share_row",
                    #"ratings_row",  # For some reason this messes resizing and fullscreen up.
                    "autogen_class_views_pdfs_upvote autogen_class_widgets_base"]

unblur = [["pageParams.blur = true", "pageParams.blur = false"],
          ["outer_page only_ie6_border blurred_page", "outer_page only_ie6_border"],
          ['unselectable="on"', ""]]


def parseArgs(argv):
    if(len(argv) != 1):
        print("Incorrect usage.\n" + 
              "Correct usage: ./hack.py [ULR | -h | --help] > [FILE.html]\n"
              "Only works on \"scribd.com/doc/\" pages!\n\n"

              "Install PHantomJS for a headless experience (sudo pacman -S phantomjs).", file=sys.stderr)
        sys.exit()

    if(argv[0] == "-h" or argv[0] == "--help"):
        print("Downloads url's webpage, unblurs pages and prints HTML.\n"
              "Only works on \"scribd.com/doc/\" pages!\n"
              "Usage: ./hack.py [ULR | -h | --help] > [FILE].html\n\n"

              "Install PHantomJS for a headless experience (sudo pacman -S phantomjs).", file=sys.stderr)
        sys.exit()

    if("scribd.com/" not in argv[0]):
        print("Url not from \"scribd.com/.\"\n" + 
              "Use -h or --help for help.", file=sys.stderr)
        sys.exit()


def removeElementByClass(className, driver):
    driver.execute_script("        var element = document.getElementsByClassName(\"" + className + "\"), i;"
                          "        for(i = element.length - 1; i >= 0; i--) {"
                          "            element[i].parentNode.removeChild(element[i]);"
                          "        }")


def startWebDriver():
    webDrivers = [webdriver.PhantomJS, webdriver.Chrome, webdriver.Firefox, webdriver.Safari, webdriver.Edge, webdriver.Opera, webdriver.Ie]

    for tryDriver in webDrivers:
        try:
            driver = tryDriver()
        except Exception as e:
            pass
        else:
            return driver

    print("No webdriver found.", file=sys.stderr)


def main(argv):
    parseArgs(argv)

    # Download page.
    driver = startWebDriver()

    driver.get(argv[0])

    driver.execute_script('document.title')

    # Remove adds, fix scaling on first page and some other minor things.
    for className in elementsToRemove:
        removeElementByClass(className, driver)

    page_source = str(driver.page_source)
    driver.quit();

    # The actual unblurring of the pages.
    for page in unblur:
        page_source = page_source.replace(page[0], page[1])

    print(page_source)
    print("\nDone!", file=sys.stderr)


if __name__ == "__main__":
    main(sys.argv[1:])
