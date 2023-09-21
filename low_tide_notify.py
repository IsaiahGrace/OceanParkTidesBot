#! /usr/bin/env python3
"""
This script gets scheduled to run by daily_noaa_fetch.py and simply selects a random message and sends it to the Telegram chat.
The message acts as a reminder to go for a walk on the beach. This script is typically scheduled to run one hour before low tide, to give plenty of time to finish up and get out there!
"""

import asyncio
import fetch_secrets as secrets
import inspect
import random
import telegram


messages = ["The tide will be low an hour! Great time to go for a walk",
            "Low tide's in one hour!",
            "Take a break and go for a walk? Low tide is soon.",
            "It's time for a walk. The tide will be low soon.",
            "The tide is *low* but I'm holdin' on\nI'm gonna be your number one",
            "Wade in the water\nWade in the water\nWade in the water, children\nGod is gonna trouble these waters",
            "Low tide in 60 minutes. Go check out the Guggenheim rocks!",
            "Perfect time for a walk! The tide is just right for a walk!",
            "Take a new boardwalk to the beach today.",
            "Go for a walk, the tide will be low soon.",
            "Is it raining? Grab a raincoat and enjoy the beach all to youself!",
            "If there’s heaven for me, I’m sure it has a beach attached to it.\n    - Jimmy Buffet",
            "The ocean makes me feel really small and it makes me put my whole life into perspective.\n    - Beyoncé",
            "Take a stroll to the creek.",
            "Time for a walk!",
            "Take you eyes off the Java code and take a walk on the beach",
            "There’s no place like home. Except the beach.",
            "All I need is a good dose of vitamin sea.",
            "The beach is calling and I must go.",
            "Cancel you meeting and take a walk!",
            "I followed my heart and it lead me to the beach.",
            "Life takes you down many paths but my favorite ones lead to the beach.",
            "Long time no sea.",
            "Seas the day.",
            "I got 99 problems but a beach ain’t one.",
            "I don’t wanna be tide down.",
            "Happiness comes in waves.",
            "The oceans roar is music to the soul.",
            "Live in the sunshine, swim the sea, drink the wild air.\n    – Ralph Waldo Emerson",
            "The beach: as close to heaven as you can get",
            "You are not a drop in the ocean. You are the entire ocean in a drop.\n    – Rumi",
            "If you’re lucky enough to live by the sea, you’re lucky enough.",
            "To rise at daybreak and feel the sunshine as it warms my skin, the soothing sounds of waves as they kiss the shore and sand between my toes: a gentle reminder that life is good.",
            "On the beach, you can live in bliss.\n    – Dennis Wilson of the Beach Boys",
            "Ah, the smell of salt and sand. There is no elixir on this blessed earth like it.",
            "When anxious, uneasy and bad thoughts come, I go to the sea, and the sea drowns them out with its great wide sounds, cleanses me with its noise, and imposes a rhythm upon everything in me that is bewildered and confused.\n    – Rainer Maria Rilke",
            "The beach is always a good idea.",
            "Time spent at the beach is never wasted.",
            "The beach – the only place where salt lowers your blood pressure.",
            "Smell the sea, and feel the sky, let your soul and spirits fly.\n    – Van Morrison",
            "The cure for anything is saltwater – sweat, tears, or the sea.\n    – Karen Blixen",
            "In every outthrust headland, in every curving beach, in every grain of sand, there is the story of the earth.    – Rachel Carson",
            "My life is like a stroll upon the beach, as near to the ocean’s edge as I can go.\n    – Henry David Thoreau",
            "To myself I am only a child playing on the beach, while vast oceans of truth lie undiscovered before me.\n    – Isaac Newton",
            "We ourselves feel that what we are doing is just a drop in the ocean. But the ocean would be less because of that missing drop.\n    – Mother Teresa",
            "Individually we are one drop. Together we are an ocean.\n    – Ryunosuke Satoro",
            "Retirement Plan: Sell seashells by the seashore.",
            "To go out with the setting sun on an empty beach is to truly embrace your solitude.\n    – Jeanne Moreau",
            "Of all the paths you take in life, make sure a few of them lead to magical sunsets at the beach.",
            "To me, the sea is a continual miracle; The fishes that swim–the rocks–the motion of the waves–the ships, with men in them, What stranger miracles are there?\n    – Walt Whitman",
            "The sea always filled her with longing, though for what she was never sure.\n    – Cornelia Funke",
            "My soul is full of longing for the secrets of the sea, and the heart of the great ocean sends a thrilling pulse through me.\n    – Henry Wadsworth Longfellow",
            "The sea possesses a power over one’s moods that has the effect of a will. The sea can hypnotize. Nature in general can do so.\n    – Henrik Ibsen",
            "Dear ocean, thank you for making us feel tiny, humble, inspired, and salty... all at once.",
            "Limitless and immortal, the waters are the beginning and end of all things on earth.\n    – Heinrich Zimmer",
            "The ocean has always been a salve to my soul...\nthe best thing for a cut or abrasion was to go swimming in salt water.\nLater down the road of life, I made the discovery that salt water was also good for the mental abrasions one inevitably acquires on land.\n    – Jimmy Buffet",
            "In one drop of water are found all the secrets of all the oceans.\n    – Kahlil Gibran",
            "The oceans roar is music to the soul.",
            "Happier than a seagull with a French fry.",
            "Let the sea set you free.",
            "Thalassophile (n) A lover of the sea, someone who loves the sea/ocean.",
            "There is pleasure in the pathless woods, there is rapture in the lonely shore, there is society where none intrudes, by the deep sea, and music in its roar; I love not Man the less, but Nature more.\n    – Lord Byron",
            "The sea does not reward those who are too anxious, too greedy, or too impatient... Patience, patience, patience, is what the sea teaches. Patience and faith. One should lie empty, open, choiceless as a beach – waiting for a gift from the sea.\n    – Anne Morrow Lindbergh",
            "There must be something strangely sacred in salt. It is in our tears and in the sea.\n    – Khalil Gibran",
            "The sea, the great unifier, is man’s only hope. Now, as never before, the old phrase has a literal meaning: we are all in the same boat.\n    – Jacques Yves Cousteau",
            "All the rivers run into the sea; yet the sea is not full\n    — Ecclesiastes 1:7",
            "You must not lose faith in humanity. Humanity is an ocean; if a few drops of the ocean are dirty, the ocean does not become dirty.\n    – Mahatma Gandhi",
            "We are all in the same boat, in a stormy sea, and we owe each other a terrible loyalty.\n    – Gilbert K. Chesterton",
            "Storms draw something out of us that calm seas don’t.\n    – Bill Hybels",
            "Time and tide wait for no man.\n    – Saint Marher",
            "Just as the wave cannot exist for itself, but is ever a part of the heaving surface of the ocean, so must I never live my life for itself, but always in the experience which is going on around me.\n    – Albert Schweitzer",
            "The sea, once it casts its spell, holds one in its net of wonder forever.\n    – Jacques Yves Cousteau",
            "The heart of man is very much like the sea, it has its storms, it has its tides and in its depths, it has its pearls too.\n    – Vincent van Gogh",
            "Oh God, your sea is so great, and my boat is so small.\n    - Breton fisherman's prayer",
            "We are tied to the ocean. And when we go back to the sea, whether it is to sail or to watch - we are going back from whence we came.\n    - John F. Kennedy",
            "Ocean is more ancient than the mountains and freighted with the memories and the dreams of Time.\n    - H. P. Lovecraft",
            "How inappropriate to call this planet Earth when it is clearly Ocean.\n    - Arthur C. Clarke",
            "The three great elemental sounds in nature are the sound of rain, the sound of wind in a primeval wood, and the sound of outer ocean on a beach.\n    - Henry Beston",
            "Ocean Park is nice.",
            ]


async def main():
    message = random.choice(messages)
    token = secrets.get_token()
    chat_id = secrets.get_chat_id()

    bot = telegram.Bot(token=token)
    if inspect.iscoroutinefunction(bot.sendMessage):
        await bot.sendMessage(chat_id=chat_id, text=message)
    else:
        bot.sendMessage(chat_id=chat_id, text=message)
    print(message)


if __name__ == "__main__":
    asyncio.run(main())
