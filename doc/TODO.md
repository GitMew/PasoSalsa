# TODO
- Package needs a better layout asap
- Follower steps:
  - Add them to all figures. (This is not trivial because I don't even know them.)
  - Have an easy way of defining the follower's starting position
  - Visualise leader+follower, only leader, only follower.
- Smart bendy arrows (can probably figure this out based on clockwise vs counterclockwise)
- In-place rotating arrows
- For figures like enchufla, there should be a difference between a clockwise and a counterclockwise half-turn.
  - Similarly: we have turns that can be over 360°. The arrows should spiral then.
- For figures like crusado, there is an "alternate" base.
- Disambiguation for leg crosses.
  - Imagine a grid `| L |  | R |`. Now it turns into `| R |  | L |`. How can we know the bend of the arrows that follow?
    Extra difficulty: if the person rotates 180°, their legs become untangled and they can do any move again.
- Coarse-grained view (i.e. just leader-follower, not the feet)
- Sequencer