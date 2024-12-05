# TODO
- Add missing patterns. (For DQN, use the infamous video.)
  - "Balancing step", but I don't know what it is in Spanish.
  - Pa'-ti pa'-mi step (if it's called that, at least)
  - Possibly, both exhibela and sacala have a "walking vuelta derecha" rather than being in-place.
- Exhibela doesn't end in caida. Something ain't right.
- Smarter arrows:
  - Bendy arrows (can probably figure this out based on clockwise vs counterclockwise)
  - In-place rotating arrows. Right now, it's hard to spot that a letter has turned by a certain angle.
  - For figures like enchufla, there should be a difference between a clockwise and a counterclockwise half-turn.
    - Similarly: we have turns that can be over 360°. The arrows should spiral then.
  - Disambiguation for leg crosses.
    - Imagine a grid `| L |  | R |`. Now it turns into `| R |  | L |`. How can we know the bend of the arrows that follow?
      Extra difficulty: if the person rotates 180°, their legs become untangled and they can do any move again.
- For figures like crusado, there is an "alternate" base.
  - Actually, it might be better to have a "simulated base" and a "canonical base". You don't need to clarify that crusado
    can start in crossed legs because that's what it ends in when you simulate it.
- Coarse-grained view (i.e. just leader-follower, not the feet)