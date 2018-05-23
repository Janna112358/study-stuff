# The Friendship Algorithm

print 'The Friendship Algorithm by Dr. Sheldon Cooper, Ph.D'
print 'Place phone call'
ans1 = raw_input('Home? ')
while ans1 != 'yes' and ans1 != 'no':
    print 'Invalid answer'
    ans1 = raw_input('Home?')
if ans1 == 'no':
        print 'Leave message and wait for callback'  
while ans1 == 'no':
    ans1 = raw_input('Phone? ')
    while ans1 != 'yes' and ans1 != 'no':
        print 'Invalid answer'
        ans1 = raw_input('Phone? ')
print 'Ask: Would you like to share a meal?'      
ans2 = raw_input('What is the response? ')
while ans2 != 'yes' and ans2 != 'no':
    print 'Invalid answer'
    ans2 = raw_input('What is the response? ')
if ans2 == 'yes':
        print 'Dine together'
        print 'BEGIN FRIENDSHIP!'
elif ans2 == 'no':
    print 'Ask: Do you enjoy a hot beverage?'
    ans3 = raw_input('What is the response? ')
    while ans3 != 'yes' and ans3 != 'no':
        print 'Invalid answer'
        ans3 = raw_input('What is the response? ')
    if ans3 == 'yes':
        ans4 = raw_input('Tea, coffee or cocoa? ')
        while ans4 != 'tea' and ans4 != 'coffee' and ans4 != 'cocoa':
            print 'Invalid answer'
            ans4 = raw_input('Tea, coffee or cocoa? ')
        if ans4 == 'tea':
            print 'Have tea'
        elif ans4 == 'coffee':
            print 'Have coffee'
        elif ans4 == 'cocoa':
            print 'Have cocoa'
        print 'BEGIN FRIENDSHIP!'
    elif ans3 == 'no':
        count = 0
        print 'Ask for recreational activity: Tell me one of you interests'
        ans5 = raw_input('Do you share that interest? ')
        while ans5 != 'yes' and count < 6:
            while ans5 != 'yes' and ans5 != 'no':
                print 'Invalid answer'
                ans5 = raw_input('Do you share that interest? ')
            if ans5 == 'no':
                count += 1
                print 'Ask for recreational activity: Tell me one of you interests'
                ans5 = raw_input('Do you share that interest? ')
        if ans5 != 'yes':
            print 'Choose least objectionable activity'   
        print "Propose: Why don't we do that together?"
        print 'Partake in interest'
        print 'BEGIN FRIENDSHIP!'
    

