

with open("big.txt", "r") as txtfile:
    for corpus_line in txtfile:
        corpus_line = corpus_line.lower().strip() # Change all alphabets to lower case, then remove leading and/or trailing whitespace(s)
        for char in corpus_line:
            if char in badchars: 
                if (char == chr(39)) and (("n"+char+"t") or (char+"s") in corpus_line): # Keep the punctuation on contraction words, e.g. "don't", "can't", "engineer's", etc.
                    continue
                else:
                    corpus_line = corpus_line.replace(char," ") # Remove digits and punctuation from all other words
        corpus_list_raw += corpus_line.split()

# Remove unwanted characters from corpus words that might still exist due to the addition of contraction words

global corpus_list = [corpus_word.strip(badchars) for corpus_word in corpus_list_raw]

# Measure word distance(s) between input word and corpus word(s)

def worddistance(word, corpus_word):
    """Measures the difference between two words and returns an integer value as word distance"""
    
    global word_distance
    word_distance = 0
    
    # Compare input word and a word from the corpus, letter by letter
    
    if len(word) == len(corpus_word):
        for i in range(len(word)):
            if word[i] != corpus_word[i]:
                word_distance += 1
                
    # If corpus word is one letter shorter than input word, append a whitespace to the end of it to facilitate comparison
    
    elif len(word) - len(corpus_word) == 1:
        corpus_word_temp = corpus_word + " " 
        for i in range(len(word)):
            if word[i] != corpus_word_temp[i]:
                word_distance += 1

    elif len(corpus_word) - len(word) == 1:
        word_temp = word + " "
        for i in range(len(word_temp)):
            if word_temp[i] != corpus_word[i]:
                word_distance += 1
    
    return word_distance

def autocorrect(word):
    """Checks if input word is in corpus: if not, measures word distance and provides nearest word suggestions (if any)"""

    # Convert input word to lower case
    
    word = word.lower()
    
    # If input word contains unwanted character(s), print a reminder statement
    
    for char in badchars:
        if char in word and (char == word[0] or char == word[-1]): 
            return str("Only alphabets allowed in word. Contraction words are exceptions. Try again.")
    
    # If input word is a single letter, print statement without calling worddistance()
    
    if (len(word) ==  1) and (word in alphabets): 
        return str("The spelling is correct")
    
    # If input word is in corpus, print statement without calling worddistance()
    
    elif word in corpus_list:
        return str("The spelling is correct")
    
    # In all other cases, invoke worddistance() to measure word differences
    
    else:
        # Initialize lists for storing suggested words later on
        
        suggested_words_initial = []
        suggested_words_temp = []
        
        for corpus_word in corpus_list:
            worddistance(word, corpus_word)
            if len(word) == 3: # If input word is of length 3, only return word suggestions that are of the same length or 1 letter less
                if word_distance == 1: 
                    suggested_words_initial.append(corpus_word)
            else:  # For all other cases, return word suggestions that are of word distance 1 or 2
                if (1 <= word_distance <= 2) and (len(word) == len(corpus_word)): 
                    suggested_words_initial.append(corpus_word) 
                elif (word_distance == 1) and ((len(word) - len(corpus_word) == 1) or (len(corpus_word) - len(word) == 1)):
                    suggested_words_initial.append(corpus_word)
                else:
                    continue
        
        # Convert list to set to remove duplicates, then convert back to list again
        
        suggested_words_temp = list(set(suggested_words_initial))
        
        # List comprehension used to generate and store tuples. A tuple consists of the frequency of suggested word in big.txt and the suggested word itself
        
        suggested_words = [(corpus_list.count(suggested_word), suggested_word) for suggested_word in suggested_words_temp]
        
        # The tuples above are stored with word frequency being in index 0 so that sorting could be performed. Most possible word(s) are listed in descending order
        
        suggested_words.sort(reverse = True)
        
        # Generate output depending on the length of word suggestion list
        
        if len(suggested_words) == 0:
            return str("No suggestion available")
            #addword(word)
        
        elif len(suggested_words) == 1:
            return str("Did you mean: {}?".format(str(suggested_words[0][1])))
            #addword(word)
            
        else:
            return str("The most likely word is: {}".format(str((max(suggested_words))[1])))
            #message_to_print = "Did you mean: "
            #for word_tuple in suggested_words:
            #    if word_tuple != suggested_words[-1]:
            #        net_time = time.process_time()-start_time
            #        message_to_print += (word_tuple[1] + ", ")
            #    else:
            #        message_to_print += ("or " + word_tuple[1] + "?")
            #        print(message_to_print)
            #        print("The most likely word is: {}".format(str((max(suggested_words))[1])))
            #        print("Done in {:0.3f} sec".format(net_time))
            #        addword(word)
