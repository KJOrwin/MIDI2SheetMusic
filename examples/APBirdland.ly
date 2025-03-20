% Find a way to have ties across repeats

\version "2.25.12"

\header {
    title = "Birdland"
}

%Saxophone
saxPart = \new Staff \with {
    instrumentName = "Alto Saxophone"
    shortInstrumentName = "A Sax."
    midiInstrument = #"alto sax"
} \notemode {
    \clef treble
    \key d \major
    \time 4/4
    \tempo 4 = 156
    \repeat volta 3 {
        R1*3
        \alternative {
            \volta 1,2 { R1 }
            \volta 3 { R1 }
        }
    }
    \repeat volta 4 {
        c'''8\repeatTie\mf b''8-- c'''8-- b''8-- a''4-- fis''8-^ a''8->~
        a''4 fis''4-^ a''4-^ b''8-- c'''8->~
        c'''4 b''4-^ a''4-^ fis''8-- e''8-^
        \alternative {
            \volta 1,2,3 { r8 fis''4.~ fis''4 r8 c'''8\mf }
            \volta 4 { r8 d''4.~ d''4 r8 f''8->~\ff }
        }
    }
    f''4 e''8-- e''8-^ r4 r8 e''8->~
    e''4 d''8-- d''8-^ r4 r8 e''8->~
    e''8 e''8-> c''8-- c''8-^ r4 r8 e''8->~
    e''4 d''8-- d''8-^ r4 r8 e''8->~
    e''4 d''8-- d''8-^ r4 r8 f''8->~
    f''4 e''2.
    r8 d''8-^ e''8-^ eis''8-^ fis''8 r8 d''8 r8
    f''8 r8 e''2 r4
}

%Cornet
cornetPart = \new Staff \with {
    instrumentName = \markup { "B" \smaller \flat " Cornet" }
    shortInstrumentName = \markup { "B" \flat "Cnt." }
    midiInstrument = #"trumpet"
} \notemode {
    \clef treble
    \key g \major
    \time 4/4
    \tempo 4 = 156
    \repeat volta 3 {
        R1*3
        \alternative {
            \volta 1,2 { R1 }
            \volta 3 { r2 r4 r8 bes'8~\mf }
        }
    }
    \repeat volta 4 {
        bes'8 a'8-- bes'8-- a'8-- g'4-- e'8-^ g'8->~ |
        g'4 e'4-^ g'4-^ a'8-- bes'8--~ |
        bes'4 a'4-^ g'4-^ e'8-- d'8-^ |
        \alternative {
            \volta 1,2,3 { r8 g'4.~ g'4 r8 bes'8 }
            \volta 4 { r8 bes'4.~ bes'4 r8 bes''8->~\ff }
        }
    } 
    bes''4 a''8-- a''8-^ r4 r8 a''8->~
    a''4 g''8-- g''8-^ r4 r8 a''8->~
    a''8 a''8-> f''8-- f''8-^ r4 r8 a''8->~
    a''4 g''8-- g''8-^ r4 r8 a''8->~
    a''4 g''8-- g''8-^ r4 r8 bes''8->~
    bes''4 a''2.
    r8 g''8-^ a''8-^ ais''8-^ b''8 r8 g''8 r8
    bes''8 r8 a''2 r4
}

%Trombone
tromPart = \new Staff \with {
    instrumentName = "Trombone"
    shortInstrumentName = "Tbn."
    midiInstrument = #"trombone"
} \notemode {
    \clef bass
    \key f \major
    \time 4/4
    \tempo 4 = 156
    \repeat volta 3 {
        R1*3
        \alternative {
            \volta 1,2 { R1 }
            \volta 3 { R1 }
        }
    }
    \repeat volta 4 {
        R1*3
        \alternative {
            \volta 1,2,3 { R1 }
            \volta 4 { r2 r4 r8\ff f'8->~ }
        }
    }
    f'4 ees'8-- ees'8-^ r4 r8 ees'8->~
    ees'4 des'8-- des'8-^ r4 r8 ees'8->~
    ees'8 ees'8-> c'8-- c'8-^ r4 r8 ees'8->~
    ees'4 des'8-- des'8-^ r4 r8 ees'8->~
    ees'4 d'8-- d'8-^ r4 r8 f'8->~
    f'4 ees'2.
    r8 d'8-^ ees'8-^ e'8-^ f'8 r8 d'8 r8
    f'8 r8 ees'2 r4
}

%Drums
%\repeat percent would be used here but nested repeats don't work well!
bottom_drumPart = \drummode {
    \voiceOne
    \tempo 4 = 156
    \repeat volta 3 {
        hhc8\mf hho8 hhc8 hho8 hhc8 hho8 hhc8 hho8
        hhc8 hho8 hhc8 hho8 hhc8 hho8 hhc8 hho8
        hhc8 hho8 hhc8 hho8 hhc8 hho8 hhc8 hho8
        \alternative {
            \volta 1,2 { hhc8 hho8 hhc8 hho8 hhc8 hho8 hhc8 hho8 }
            \volta 3 { hhc8 hho8 hhc8 hho8 hhc8 hho8 hhc8 hho8 }
        }
    }
    \repeat volta 4 {
        <hhc sn>8 hho8 <hhc sn>8 hho8 <hhc sn>8 hho8 <hhc sn>8 hho8
        <hhc sn>8 hho8 <hhc sn>8 hho8 <hhc sn>8 hho8 <hhc sn>8 hho8
        <hhc sn>8 hho8 <hhc sn>8 hho8 <hhc sn>8 hho8 <hhc sn>8 hho8
        \alternative {
            \volta 1,2,3 { <hhc sn>8 hho8 <hhc sn>8 hho8 <hhc sn>8 hho8 <hhc sn>8 hho8 }
            \volta 4 { \repeat percent 9 { <hhc sn>8 hho8 <hhc sn>8 hho8 <hhc sn>8 hho8 <hhc sn>8 hho8 } }
        }
    }
}

top_drumPart = \drummode {
    \voiceTwo
    \tempo 4 = 156
    \repeat volta 3 {
        \skip R1*3
        \alternative {
            \volta 1,2 { \skip R1 }
            \volta 3 { \skip R1 }
        }
    }
    \repeat volta 4 {
        \skip R1*3
        \alternative {
            \volta 1,2,3 { \skip R1 }
            \volta 4 { \skip r2 \skip r4 \skip r8 rb8~\ff }
        }
    }
    rb4 rb8 rb8 r4 r8 rb8->~
    rb4 rb8 rb8 r4 r8 rb8->~
    rb4 rb8 rb8 r4 r8 rb8->~
    rb4 rb8 rb8 r4 r8 rb8->~
    rb4 rb8 rb8 r4 r8 rb8->~
    rb4 rb2.
    r8 rb8-^ rb8-^ rb8-^ rb8 r8 rb8 r8
    rb8-> r8 rb2 r4
}

drumPart = \new DrumStaff \with {
    instrumentName = "Drums"
    shortInstrumentName = "Drm."
    midiInstrument = #"standard kit"
} \new DrumVoice <<
    \top_drumPart
    \bottom_drumPart
>>

%Piano
pianoPart = \new PianoStaff \with {
    instrumentName = "Piano"
    shortInstrumentName = "Pno."
} <<
    \new Staff \with {
        midiInstrument = #"acoustic grand"
    } \notemode {
        \clef treble
        \key f \major
        \time 4/4
        \tempo 4 = 156
        \repeat volta 3 {
            R1*3
            \alternative {
                \volta 1,2 { R1 }
                \volta 3 { R1 }
            }
        }
        \repeat volta 4 {
            R1*3
            \alternative {
                \volta 1,2,3 { R1 }
                \volta 4 { r2 r4 r8\ff <c' f' aes'>8->~ }
            }
        }
        <c' f' aes'>4 <bes ees' g'>8-- <bes ees' g'>8-^ r4 r8 <bes ees' g'>8->~
        <bes ees' g'>4 <aes des' f'>8-- <aes des' f'>8-^ r4 r8 <bes ees' g'>8->~
        <bes ees' g'>4 <g c' ees'>8-- <g c' ees'>8-^ r4 r8 <bes ees' g'>8->~
        <bes ees' g'>4 <aes des' f'>8-- <aes des' f'>8-^ r4 r8 <bes ees' g'>8->~
        <bes ees' g'>4 <a d' f'>8-- <a d' f'>8-^ r4 r8 <c' f' aes'>8->~
        <c' f' aes'>4 <bes ees' g'>2.
        r8 <a d' f'>8-^ <bes ees' g'>8-^ <b e' gis'>8-^ <c' f' a'>4-> <a d' f'>4->
        <c' f' aes'>4-> <bes ees' g'>2 r8 <f f'>8-^
    }
    \new Staff \notemode {
        \set Staff.midiInstrument = #"synth bass 1"
        \clef bass
        \key f \major
        \time 4/4
        \tempo 4 = 156
        \repeat volta 3 {
            a,2\mf bes,4. c8~ |
            c2.~ c8 a,8~ |
            a,2 bes,4 c8 f8~ |
            \alternative {
                \volta 1,2 { f2.~ f8 a,8 }
                \volta 3 { f2.~ f8 a,8~ }
            }
        } 
        \repeat volta 4 {
            a,2 bes,4. c8~ |
            c2.~ c8 a,8~ |
            a,2 bes,4 c8 f8~ |
            \alternative {
                \volta 1,2,3 { f2.~ f8 a,8 }
                \volta 4 { f2. r8\ff \set Staff.midiInstrument = #"acoustic grand" \ottava #-1 f,,8->~ }
            }
        }
        f,,4 r4 r8 g,,4-^ aes,,8->~
        aes,,4 r4 r8 aes,,8 bes,,8 c,8->~
        c,4 r8 f,,8-^ r8 g,,8-^ r8 bes,,8->~
        bes,,2 r8 g,,8 aes,,8 a,,8->~
        a,,8 c,8 d,8 f,8-^ r4 r8 bes,,8-^
        r8 c,8-^ des,2.
        r8 f,,8-^ r8 g,,8-^ r8 aes,,8-^ r8 a,,8-^
        r8 c,4-> r8 r2
        \ottava #0
    }
>>

%Bass
bassPart = \new Staff \with {
    instrumentName = "Bass Guitar"
    shortInstrumentName = "B Gui."
    midiInstrument = #"electric bass (finger)"
} \notemode {
    \clef bass
    \key f \major
    \time 4/4
    \tempo 4 = 156
    \repeat volta 3 {
        a,2\mf bes,4. c8~ |
        c2.~ c8 a,8~ |
        a,2 bes,4 c8 f8~ |
        \alternative {
            \volta 1,2 { f2.~ f8 a,8 }
            \volta 3 { f2.~ f8 a,8~ }
        }
    } 
    \repeat volta 4 {
        a,2 bes,4. c8~ |
        c2.~ c8 a,8~ |
        a,2 bes,4 c8 f8~ |
        \alternative {
            \volta 1,2,3 { f2.~ f8 a,8 }
            \volta 4 { f2. r8\ff f,8->~ }
        }
    }
    f,4 r4 r8 g,4-^ aes,8->~
    aes,4 r4 r8 aes,8 bes,8 c8->~
    c4 r8 f,8-^ r8 g,8-^ r8 bes,8->~
    bes,2 r8 g,8 aes,8 a,8->~
    a,8 c8 d8 f8-^ r4 r8 bes,8-^
    r8 c8-^ des2.->
    r8 f,8-^ r8 g,8-^ r8 aes,8-^ r8 a,8-^
    r8 c4-> r8 r4 r8 f8->
}

\score {
    <<
        \saxPart
        \new StaffGroup <<
            \cornetPart
            \tromPart
        >>
        \drumPart
        \pianoPart
        \bassPart
    >>
    \layout { }
}    

\score {
    <<
        \transpose c ees {
            \unfoldRepeats {
                \saxPart
            }
        }
        \transpose c bes {
            \unfoldRepeats {
                \cornetPart
            }
        }
        \unfoldRepeats {
            \tromPart
        }
        \unfoldRepeats {
            \drumPart
        }
        \unfoldRepeats {
            \pianoPart 
        }
        \unfoldRepeats {
            \bassPart
        }
    >>
    \midi {
        \context {
            \Score midiChannelMapping = #'instrument
        }
    }
}