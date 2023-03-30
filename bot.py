from selenium import webdriver
from time import sleep
from secret import pw
from random import randint
from random import shuffle

class Bot():

    links = []
    #comments = ['Nice!', 'Sick!']

    #Used as a boundery to check how many actions have been processed
    totalActionCount = 0
    currentlyFollowedCount = 0
    currentlyLikedCount = 0

    #Instagram hashtags
    hashtags = ['200sx', 'Carporn', 'Silvia','S14','JDM','Automotive',
    'Nissan','Drifting','Jdmnation','Hellaflush','Stance','Low','240sx','180sx','Slammed','Supra','Mazdarx7','Hotboi']

    #Instagram accounts
    accounts = ['headturnersuk', 'mpireuk', 'ozygti', 'nissan_200sx', 'tucked_', 'jdmvibe', 'v3locity__',
    'officialslammeduk', 'illiminate', 'nightride.pl', 'mishimoto', 'workwheelsjapan', 'tjhunt_', 'adamc3046', 'adam_lz', 
    'thebritishdriftchampionship', 'silviarepublic_', 'x28sarahmep']

    def __init__(self):
        print('--\n--\n--\nWelcome to Barts instaBot, updated will be printed here')
        
        #Login
        self.instaLogin()

        #Shuffle the lists so its in a random order
        shuffle(self.hashtags)
        shuffle(self.accounts)

        #Counter used to loop round hashtags and accounts
        counter = 0
        #While loop until there are no more accounts or hashtags
        while counter < len(self.hashtags) and counter < len(self.accounts):
            #Only perform 30 actions or wait 1 hour
            if self.totalActionCount <= 25:
                sleep(10)
                print('\nCurrently liking pictures and following users from #' + self.hashtags[counter])
                self.like_comment_by_hashtag(self.hashtags[counter])
                print('Currently liked ' + str(self.currentlyLikedCount) + ' picstures and followed ' + str(self.currentlyFollowedCount))

                sleep(10)
                print('\nCurrently following followers from ' + self.accounts[counter])
                self.followFollowersFromAccount(self.accounts[counter], 10)
                print('Currently followed ' + str(self.currentlyFollowedCount))
                
                sleep(10)
                print('\nCurrently following followers from ' + self.accounts[counter] + ' recent picture')
                self.followFollersRecentLikes(self.accounts[counter], 10)
                print('Currently liked ' + str(self.currentlyLikedCount) + ' picstures and followed ' + str(self.currentlyFollowedCount))

                counter += 1
            else:
                #Wait 1 hour 1 minutes
                print('Warning! Limit reached, waiting 1 hour 1 minute...')
                sleep(3660)
                self.totalActionCount = 0

    def instaLogin(self):
        self.driver = webdriver.Chrome()
        self.driver.get('https://www.instagram.com/')

        #Accept cookie
        sleep(10)
        accept_cookie = self.driver.find_element_by_xpath('/html/body/div[2]/div/div/div/div[2]/button[1]')
        accept_cookie.click()

        #Input username
        sleep(2)
        inputUsername = self.driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[1]/div/label/input')
        inputUsername.send_keys('ENTER USERNAME HERE')
        
        #Input password
        sleep(2)
        inputPassword = self.driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[2]/div/label/input')
        inputPassword.send_keys(pw)

        #Press login
        sleep(10)
        login = self.driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[3]/button')
        login.click()

        #Password save button doesn't always show up
        #Press dont save pass
        try:
            sleep(10)
            dontSavePass = self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div/div/div/button').click()
        except:
            #No need to inform anyone about this
            print("Warning: Save password did not show up")

        #Turn off notifactions
        sleep(10)
        offNotification = self.driver.find_element_by_xpath('/html/body/div[4]/div/div/div/div[3]/button[2]')
        offNotification.click()

    def like_comment_by_hashtag(self, hashtag):
        #Get links of top pics under hashtag
        self.driver.get('https://www.instagram.com/explore/tags/{}/'.format(hashtag))
        links = self.driver.find_elements_by_tag_name('a')

        #Condition to only get the correct links
        def condition(link):
            return '.com/p/' in link.get_attribute('href')
        valid_links = list(filter(condition, links))

        def condition(link):
            return '.com/p/' in link.get_attribute('href')
        valid_links = list(filter(condition, links))

        for i in range(19):
            link = valid_links[i].get_attribute('href')
            if link not in self.links:
                self.links.append(link)

        likedCount = 0
        for link in range(9, len(self.links)):
            likedCount += 1

            sleep(10)
            #Open page
            self.driver.get(self.links[link])

            #Like picture
            sleep(10)
            self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div[1]/article/div[3]/section[1]/span[1]/button').click()
    
            #Follow user
            #Check if user isn't already followed
            sleep(10)
            buffer = self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div[1]/article/header/div[2]/div[1]/div[2]/button')
            if buffer.text == "Follow":
                buffer.click()
                self.currentlyFollowedCount += 1

            #Update amount of liked pictures
            self.totalActionCount += 1
            self.currentlyLikedCount += 1
            sleep(10)

    #Method to follow a users followers
    def followFollowersFromAccount(self, searchUsername, amount):
        #Get links of top pics under hashtag
        self.driver.get('https://www.instagram.com/{}/'.format(searchUsername))

        #Go to Instagram account
        sleep(5)
        self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a/span').click()

        #Loop to follow users
        for i in range(1, amount + 1):
            sleep(10)
            buffer = self.driver.find_element_by_xpath('/html/body/div[5]/div/div/div[2]/ul/div/li[' + str(i) + ']/div/div[3]/button')
            if buffer.text == "Follow":
                #Follow user
                buffer.click()

                self.totalActionCount += 1
                self.currentlyFollowedCount += 1

                sleep(1)
        
        #Second picture
        #HBoOv

    def followFollersRecentLikes(self, searchUsername, amount):
        sleep(5)
        self.driver.get('https://www.instagram.com/{}/'.format(searchUsername))

        #Click first image
        sleep(5)
        self.driver.find_element_by_class_name("_9AhH0").click()

        try:
            #Click on likes
            sleep(5)
            self.driver.find_element_by_xpath("/html/body/div[5]/div[2]/div/article/div[3]/section[2]/div/div/a").click()

            #Loop to follow users
            for i in range(1, amount + 1):
                sleep(10)

                buffer = self.driver.find_element_by_xpath('/html/body/div[6]/div/div/div[2]/div/div/div[' + str(i) + ']/div[3]/button')
                if buffer.text == "Follow":
                    buffer.click()

                    self.totalActionCount += 1
                    self.currentlyFollowedCount += 1

                sleep(1)

        except:
            #Video is currently not supported
            print('Video liking is not supported, trying next image')

            #Try again with the next picture
            try:
                #Reload the profile again
                sleep(5)
                self.driver.get('https://www.instagram.com/{}/'.format(searchUsername))

                #Click second image
                sleep(5)
                self.driver.find_element_by_class_name("HBoOv").click()
                
                #Click on likes
                sleep(5)
                self.driver.find_element_by_xpath("/html/body/div[5]/div[2]/div/article/div[3]/section[2]/div/div/a").click()

                #Loop to follow users
                for i in range(1, amount + 1):
                    sleep(10)

                    buffer1 = self.driver.find_element_by_xpath('/html/body/div[6]/div/div/div[2]/div/div/div[' + str(i) + ']/div[3]/button')
                    if buffer1.text == "Follow":

                        self.totalActionCount += 1
                        self.currentlyFollowedCount += 1

                    sleep(1)
            except:
                #Video is currently not supported
                print('Video liking is not supported, trying next image')
                print('Account skipped')
               
def main():
    my_bot = Bot()

if __name__ == '__main__':
    main()
