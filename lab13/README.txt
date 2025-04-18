Caleb Koutrakos - 253300

Minimum Specifications (Statement of Work)

1. A Single Player - This is the game character that the user will play, which must:
    a. Player must be a sprite which is normally in an animation loop
       -I will use the ninja sprite given in the labs and have him to do most, if not all, of the animations depending on the situation he is in:
        -He will attack when prompted by user and when unlocked
        -Possibly climb when up against a wall and user prompts it (possible unlock in later levels?)
        -Will use the dead animation after dying and waiting to respawn
        -Possibly glide when prompted by user (unlock in later levels)
        -Will be idle when stationary on ground, receiving no interaction from user, enemies, or environment
        -Will jump when user prompts it and when falling. Will likely only use half of full animation when falling
        -Will jump-attack after user prompts jump and whilst still in air, user prompts attack. Possibly will allow it when the ninja is falling, with no user prompted jump required beforehand
        -Will jump-throw when throwing is unlocked and when ninja is in the air, after falling or after jumping and still in the air akin to the jump-attack
        -Will run when unlocked and user is pressing lateral movement buttons on the ground
        -Will slide when laterally moving and user prompts with slide buttons
        -Will throw when unlocked and user is on the ground and prompts with throw button
    b. Sprites should face in the direction of movement
        -I will use the feature which was already implemented in the lab to ensure that all entities (player, enemies, projectiles) face the correct direction which will mostly be the direction they are moving in
    c. Be movable in the x and y directions, z is optional, controlled by keyboard input (use the arrow keys as well as any other keys you need for actions)
        -I will use the arrow keys and WASD interchangably, shift for moving faster, space for jumping, some other button for slide and another for glide
    d. Have the ability to "shoot" or "throw" something that can harm enemies.
        -I will allow the user to throw a kunai/star after the weapon is unlocked. I will make the projectile its own entity akin to player and enemies and will use the proper animations facing the proper direction
    e. Must have the concept of HP (Health Points) so that a single hit to the player doesnt cause insta-death
        -I will have a health bar consisting of hearts or something on the screen which will decrease when hit
    f. Movement must be somewhat grounded in reality, (ex. jumps, running, walking, flying, should all look like one would expect)
        -I will use the projectile motion formulas to ensure everything appears natural. I will have to modify it slightly to ensure the gameplay is fun but the general implementation will be consistent with mathematical reality

2. Enemies - These are the opposing players that the computer runs, which must:
    a. Enemy must be a sprite which is normally in an animation loop
        -As tediously mentioned with the player, I will implement all of the animations: attack, idle, run, dead; when appropriate
    b. Sprites should face in the direction of movement
        -I will use the previously mentioned and lab implemented method to accomplish this
    c. Be movable in the x and y directions, z is optional.
        -I will use x and y and allow the enemies to move laterally on their own with some basic AI which repeats, follows player, or detects edges like the red koopas in Mario
    d. Have some ability to attack the Player
        -I will use the attack animation when they are close enough to the player. If I implement ranged ability for the enemies then I will do the same for their ranged projectiles
    e. Must have the concept of HP (Health Points) so that a single hit from the player doesnt cause insta-death
        -HP will be dependent on enemies. I think most will be one hit, but at the end, or some smaller encounters, I will implement a health bar over their heads or below them and deduct health based on player attacks which connect with the enemy
    f. Movement must be somewhat grounded in reality, (ex. jumps, running, walking, flying, should all look like one would expect)
        -As mentioned, I will use the projectile motion formulas with modified accelerations and velocities to ensure things are fun
    g. There must be some movement to the enemies
        -The enemies will move as previously mentioned: track the player, move side to side on a platform, turn around when hitting a wall, repeat a patrol like pattern, etc. Basic AI

3. Environment - The environment that the game takes place in must:
    a. Have some obstacles such as terrain that the Players and Enemies cant move through
        -I will have platforms which the player will jump to, and down to, some areas possibly requiring the glide or slide, and will have holes that mean death. I may also try to implement some spike traps which will be functionally equivalent to holes.

Overall my game will use premade sprites and a lot of stuff from labs and class. I will use the Ninja as the player and I will mainly use zombies but will likely find some other sprites for more enemies and maybe bosses. The game will either be Mario style levels, or open metroidvania style world. The end state would be that the player can unlock abilities like attacks and movements so that they can explore stuff and do things previously unable. This is more conducive to a metroidvania style but could also work with Mario style. If I do Mario style, I will have 3-10 levels, depending on the size will determine how many.

I will achieve all the minimum functionality before I work on designing the world and implementing extra features like gliding.