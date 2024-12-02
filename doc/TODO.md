# TODO
- Transformations for easier reuse:
  - "Leader/follower like this figure". Possibly, a `Figura` should actually be built from a pair of more fundamental 
    building blocks, e.g. a `Guapea` figura would be a pair of `LeaderGuapea` and `FollowerGuapea` blocks. Examples:
    - The leader steps in first 8 counts of sacala are just an enchufla
    - The follower steps in exhibela are just sacala, after she has rotated, which in turn is just a vuelta derecha
    - PasealaEnFrente is literally leader crusado and follower Cuban basic.
  - "Mirror of this block", e.g. `FollowerGueapea` and `FollowerCubanBasic` are just mirrors of `LeaderGuapea` and `LeaderCubanBasic`.
- Follower steps:
  - Add them to all figures. (This is not trivial because I don't even know them.)
  - Have an easy way of defining the follower's starting position
  - Visualise leader+follower, only leader, only follower.
- Smart bendy arrows (can probably figure this out based on clockwise vs counterclockwise)
- In-place rotating arrows
- For figures like enchufla, there should be a difference between a clockwise and a counterclockwise half-turn.
  - Similarly: we have turns that can be over 360°. The arrows should spiral then.
- For figures like crusado, there is an "alternate" base.
  - Actually, it might be better to have a "simulated base" and a "canonical base". You don't need to clarify that crusado
    can start in crossed legs because that's what it ends in when you simulate it.
- Disambiguation for leg crosses.
  - Imagine a grid `| L |  | R |`. Now it turns into `| R |  | L |`. How can we know the bend of the arrows that follow?
    Extra difficulty: if the person rotates 180°, their legs become untangled and they can do any move again.
- Coarse-grained view (i.e. just leader-follower, not the feet)