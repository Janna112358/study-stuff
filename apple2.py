print 'Only yes and no answers, please.'
ans1 = raw_input('Do you like pie?: ')
while ans1 != 'yes':
    if ans1 == 'no':
        ans2 = raw_input('Are you sure?: ')
        if ans2 == 'no':
            ans1 = raw_input('Do you like pie?: ')
        elif ans2 == 'yes':
            print "No you're not"
        else: ans2 = raw_input('That is not a valid answer, please try again: ')    
    else: ans1 = raw_input('That is not a valid answer, please try again: ')
print "Me too! comme c'est curieux, comme c'est bizarre et quelle coincidence!"
ans3 = raw_input('Okay, and what about apple pie?: ')
while ans3 != 'yes':
    if ans3 == 'no':
        ans4 = raw_input('But you do like apples, right?: ')
        while ans4 != 'yes':
            if ans4 == 'no':
                ans5 = raw_input('Are you sure?: ')
                if ans5 == 'no':
                    ans4 = raw_input('But you do like apples, right?: ')
                elif ans5 == 'yes':
                    print "No you're not"
                else: ans5 = raw_input('That is not a valid answer, please try again: ')    
            else: ans4 = raw_input('That is not a valid answer, please try again: ')       
        print 'So you like apples AND pie...'
        ans3 = raw_input('Okay, and what about apple pie?: ')          
    else:
        ans3 = raw_input('That is not a valid answer, please try again: ')
print "Mais alors, mais alors, mais alors, mais alors, mais alors! We're so much alike!"
