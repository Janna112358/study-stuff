answer1=raw_input('Do you like pie?: ')
if answer1=='yes':
    answer2=raw_input('What about apple pie?: ')
    if answer2=='yes':
        print'Me too!'
    elif answer2=='no':
        print'Of course you do, who does NOT like apple pie?'
    else:
        print'That is not a valid answer, i quit'
elif answer1=='no':
    print'Not possible'
else:
    print'That is not a valid answer, i quit'
