# -*- coding: utf-8 -*-
"""
Created on Mon Feb  2 14:02:44 2026

@author: Dell
"""
import streamlit as st
import pandas as pd
#from typing_extensions import Counter

    
# Add a section for uploading text files
st.write("==================================")
st.header("Text Analyser")
st.write("==================================")

text_provided = ""

st.write("Provide text that should be analysed for readability below")
text_provided = text_provided + " " + st.text_area("Write here", "")


#st.write("or")
#uploaded_file = st.file_uploader("Upload a text file", type="txt")
#if uploaded_file:
#    text_provided = text_provided + " " + pd.read_fwf(uploaded_file)
#    #st.dataframe(publications)    

st.write("Results:")
st.write("...............")    
def count_words(myText):
  words = myText.split()
  return len(words)

def count_sentences(text):
    """Count the number of sentences (periods, question marks, exclamation marks)."""
    sentence_endings = ['.','!','?']
    total_sentences = 0  # Initialize total_sentences
    for char in text:
      if char in sentence_endings:
        total_sentences += 1
    return total_sentences  # Move return outside the loop

def count_syllables_word(word):
    """Estimate syllables in a word."""
    word = word.lower()
    vowels = 'aeiouy'

    if len(word) <= 3:
        return 1

    count = 0
    prev_was_vowel = False

    for char in word:
        is_vowel = char in vowels
        if is_vowel and not prev_was_vowel:
            count += 1
        prev_was_vowel = is_vowel

    # Adjust for silent 'e' at end
    if word.endswith('e') and count > 1:
        count -= 1

    return max(1, count)

def count_syllables(text):
    """Total syllable count across all words."""
    words = text.split()
    return sum(count_syllables_word(word) for word in words)

def calculate_readability(text):
    """
    Calculate Flesch-Kincaid readability score.
    Score = 206.835 - 1.015(total words/total sentences) - 84.6(total syllables/total words)
    """
    words = count_words(text)
    sentences = count_sentences(text)
    syllables = count_syllables(text)

    if sentences == 0 or words == 0:
        return 0.0

    avg_sentence_length = words / sentences
    avg_syllables_per_word = syllables / words

    score = 206.835 - (1.015 * avg_sentence_length) - (84.6 * avg_syllables_per_word)
    return score

def count_paragraphs(text):
    """Count the number of paragraphs (separated by blank lines)."""
    paragraphs = [p for p in text.split("\n\n") if p.strip()]
    return len(paragraphs)


def analyze_text(text):
    """
    Main analysis function - coordinates all sub-analyses.
    Returns a dictionary with all metrics.
    """
    return{
        'word_count': count_words(text),
        'sentence_count': count_sentences(text),
        'paragraph_count': count_paragraphs(text),
        'syllable_count': count_syllables(text),
        'readability_score': calculate_readability(text)
    }


if text_provided != "":
    dictResult = analyze_text(text_provided)

    for metric, value in dictResult.items():
        st.write(f"{metric.replace('_', ' ').title()}: {value}")

    st.write("")
    st.write("Decomposition demonstration:")
    st.write("  - count_words() handles word counting")
    st.write("  - count_sentences() handles sentence counting")
    st.write("  - count_paragraphs() handles paragraph counting")
    st.write("  - count_syllables() handles syllable estimation")
    st.write("  - calculate_readability() combines metrics for a score")
    st.write("  - analyze_text() coordinates everything") 