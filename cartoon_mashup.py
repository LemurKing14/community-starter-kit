"""Cartoon character mashup generator.

Run from the command line to generate a new hybrid character that blends
three randomly selected inspirations from a curated pool of cartoons,
anime, video games, and mascots.
"""

from __future__ import annotations

import argparse
import itertools
import random
from dataclasses import dataclass
from typing import Iterable, List, Sequence


# Organized pool pulled from the provided character list
CHARACTER_POOLS = {
    "The Simpsons": ["Homer Simpson", "Marge Simpson", "Bart Simpson", "Lisa Simpson"],
    "Family Guy & The Cleveland Show": [
        "Peter Griffin",
        "Lois Griffin",
        "Stewie Griffin",
        "Brian Griffin",
        "Cleveland Brown",
        "Cleveland Jr.",
        "Donna Tubbs-Brown",
        "Roberta Tubbs",
        "Rallo Tubbs",
    ],
    "Futurama": [
        "Philip J. Fry",
        "Turanga Leela",
        "Bender",
        "Professor Farnsworth",
        "Dr. John Zoidberg",
        "Amy Wong",
        "Hermes Conrad",
        "Zapp Brannigan",
        "Kif Kroker",
        "Nibbler",
        "Mom",
    ],
    "South Park": ["Eric Cartman", "Stan Marsh", "Kyle Broflovski", "Kenny McCormick"],
    "Rick and Morty": ["Rick Sanchez", "Morty Smith", "Summer Smith"],
    "King of the Hill": ["Hank Hill", "Peggy Hill", "Bobby Hill", "Dale Gribble", "Boomhauer", "Bill Dauterive"],
    "Bob’s Burgers": [
        "Bob Belcher",
        "Linda Belcher",
        "Tina Belcher",
        "Gene Belcher",
        "Louise Belcher",
        "Teddy",
    ],
    "American Dad!": ["Stan Smith", "Francine Smith", "Roger", "Steve Smith", "Hayley Smith", "Klaus Heisler"],
    "Archer": ["Sterling Archer", "Lana Kane", "Cheryl Tunt", "Pam Poovey", "Cyril Figgis", "Malory Archer"],
    "Adult Swim Classics": [
        "Master Shake",
        "Meatwad",
        "Frylock",
        "Carl Brutananadilewski",
        "Space Ghost",
        "Zorak",
        "Moltar",
        "Brak",
        "Birdman",
        "Phil Ken Sebben",
        "Peanut",
        "Captain Murphy",
        "Dr. Quinn",
        "Hesh",
        "Brock Samson",
        "Dr. Thaddeus “Rusty” Venture",
        "Hank Venture",
        "Dean Venture",
        "The Monarch",
        "Dr. Girlfriend",
        "Nathan Explosion",
        "Skwisgaar Skwigelf",
        "Pickles",
        "Toki Wartooth",
        "William Murderface",
        "Early Cuyler",
        "Rusty Cuyler",
        "Sheriff",
        "The Warden",
        "Jared",
        "Coach McGuirk",
        "Brendon Small",
        "Paula Small",
        "Robot Chicken",
        "The Nerd",
        "Tim Heidecker",
        "Eric Wareheim",
        "Xavier (Renegade Angel)",
        "Baron Underbheit",
        "Moral Orel",
        "Clay",
        "Bloberta",
        "Rev. Putty",
        "Coach Stopframe",
    ],
    "The Critic / Dr. Katz": ["Jay Sherman", "Marty Sherman", "Doris Grossman", "Jeremy Hawke", "Dr. Jonathan Katz", "Ben Katz", "Laura Silverman"],
    "SpongeBob SquarePants": ["SpongeBob SquarePants", "Patrick Star", "Squidward Tentacles", "Mr. Krabs"],
    "Rugrats": ["Tommy Pickles", "Chuckie Finster", "Phil DeVille", "Lil DeVille", "Angelica Pickles", "Susie Carmichael", "Spike"],
    "Ren & Stimpy": ["Ren Höek", "Stimpy"],
    "Hey Arnold!": ["Arnold Shortman", "Helga Pataki"],
    "Fairly OddParents": ["Timmy Turner", "Cosmo", "Wanda"],
    "Danny Phantom": ["Danny Phantom", "Vlad Plasmius"],
    "Invader Zim": ["Invader Zim", "GIR"],
    "Other Nicktoons": [
        "Rocko",
        "Heffer Wolfe",
        "Doug Funnie",
        "Skeeter Valentine",
        "Ickis",
        "Oblina",
        "Krumm",
        "CatDog",
        "Daggett",
        "Norbert",
        "Jimmy Neutron",
        "Johnny Test",
    ],
    "Adventure Time": ["Finn the Human", "Jake the Dog", "Princess Bubblegum"],
    "Regular Show": ["Mordecai", "Rigby"],
    "The Amazing World of Gumball": ["Gumball Watterson", "Darwin Watterson"],
    "Steven Universe": ["Steven Universe", "Garnet", "Pearl", "Amethyst"],
    "Powerpuff Girls": ["Blossom", "Bubbles", "Buttercup", "Mojo Jojo"],
    "Dexter’s Laboratory": ["Dexter", "Dee Dee"],
    "Johnny Bravo": ["Johnny Bravo"],
    "Courage the Cowardly Dog": ["Courage", "Eustace Bagge"],
    "Ed, Edd n Eddy": ["Ed", "Edd", "Eddy"],
    "Ben 10": ["Ben Tennyson", "Heatblast", "Four Arms"],
    "Samurai Jack": ["Samurai Jack", "Aku"],
    "Cow and Chicken / I Am Weasel": ["Cow", "Chicken", "Red Guy"],
    "Other CN/Action": ["Kim Possible", "Shego", "Jake Long", "Captain Planet", "The Tick", "Grim"],
    "Looney Tunes": [
        "Bugs Bunny",
        "Daffy Duck",
        "Elmer Fudd",
        "Marvin the Martian",
        "Porky Pig",
        "Foghorn Leghorn",
        "Wile E. Coyote",
        "Road Runner",
        "Speedy Gonzales",
        "Tasmanian Devil",
        "Sylvester",
        "Tweety",
    ],
    "Scooby-Doo": ["Scooby-Doo", "Shaggy Rogers", "Fred Jones", "Velma Dinkley"],
    "The Flintstones & The Jetsons": ["Fred Flintstone", "Wilma Flintstone", "George Jetson", "Rosie"],
    "Yogi Bear & Friends": ["Yogi Bear", "Boo-Boo Bear"],
    "Tom and Jerry": ["Tom", "Jerry", "Spike", "Tyke"],
    "Other Hanna-Barbera": [
        "Hong Kong Phooey",
        "Tinker",
        "Mark",
        "Debbie",
        "Blue Falcon",
        "Dynomutt",
        "Jonny Quest",
        "Hadji",
        "Race Bannon",
        "Zandor",
        "Tara",
        "Dorno",
        "Tundro",
        "Zok",
        "Goop",
        "Gleep",
        "Papa Smurf",
        "Smurfette",
        "Brainy",
        "Hefty",
        "Clumsy",
        "Gargamel",
        "Azrael",
        "Tyg Tiger",
        "Pammy Panda",
        "Rick Raccoon",
        "Digger Mole",
        "Tanker Elephant",
    ],
    "The Fab Five & Friends": ["Mickey Mouse", "Minnie Mouse", "Donald Duck", "Daisy Duck", "Goofy", "Pluto", "Pete"],
    "Disney Afternoon / TV": ["Scrooge McDuck", "Launchpad McQuack", "Darkwing Duck", "Chip", "Dale", "Baloo", "King Louie"],
    "Winnie the Pooh": ["Winnie-the-Pooh", "Piglet", "Tigger", "Eeyore", "Rabbit", "Owl", "Kanga", "Roo", "Christopher Robin"],
    "Pixar / Modern Movies": ["Woody", "Buzz Lightyear", "Jessie", "Mr. Potato Head", "Slinky Dog", "Rex", "Hamm", "Bo Peep", "Wreck-It Ralph", "Baymax", "Stitch"],
    "DC Comics (Justice League / Super Friends)": [
        "Superman",
        "Batman",
        "Wonder Woman",
        "Robin",
        "Aquaman",
        "Flash",
        "Green Lantern",
        "Martian Manhunter",
        "Hawkgirl",
        "Green Arrow",
        "Black Canary",
        "Wonder Twin Zan",
        "Wonder Twin Jayna",
        "Gleek",
        "Joker",
        "Harley Quinn",
        "Poison Ivy",
        "Catwoman",
        "Two-Face",
        "Penguin",
        "Riddler",
        "Scarecrow",
        "Mr. Freeze",
    ],
    "Marvel": ["Spider-Man", "Venom", "Green Goblin", "Doctor Octopus", "Sandman", "Electro", "Kingpin", "Mary Jane Watson"],
    "Teenage Mutant Ninja Turtles": ["Leonardo", "Michelangelo", "Donatello", "Raphael", "Shredder"],
    "Transformers": ["Optimus Prime", "Megatron", "Starscream", "Soundwave"],
    "G.I. Joe": ["Snake Eyes", "Cobra Commander"],
    "Masters of the Universe": ["He-Man", "Skeletor", "She-Ra"],
    "Thundercats": ["Lion-O", "Cheetara", "Mumm-Ra"],
    "Inspector Gadget": ["Inspector Gadget", "Penny Gadget"],
    "Warner Bros (Animaniacs / 90s)": [
        "Yakko Warner",
        "Wakko Warner",
        "Dot Warner",
        "Pinky",
        "The Brain",
        "Freakazoid",
        "Earthworm Jim",
        "Professor Monkey-For-A-Head",
    ],
    "Nintendo": ["Mario", "Luigi", "Yoshi", "Link", "Kirby", "Pikachu", "Charmander", "Meowth"],
    "Sega / Other": ["Sonic the Hedgehog", "Tails", "Knuckles", "Crash Bandicoot", "Spyro", "Mega Man", "Pac-Man"],
    "Anime (Mainstream)": [
        "Goku",
        "Vegeta",
        "Naruto Uzumaki",
        "Sasuke Uchiha",
        "Monkey D. Luffy",
        "Sailor Moon",
        "Ash Ketchum",
        "Astro Boy",
        "Totoro",
        "No-Face",
    ],
    "Peanuts": [
        "Charlie Brown",
        "Snoopy",
        "Woodstock",
        "Lucy van Pelt",
        "Linus van Pelt",
        "Sally Brown",
        "Schroeder",
        "Peppermint Patty",
        "Marcie",
        "Franklin",
    ],
    "Classic Icons": [
        "Popeye",
        "Olive Oyl",
        "Betty Boop",
        "Felix the Cat",
        "Pink Panther",
        "Inspector Clouseau",
        "Woody Woodpecker",
        "Buzz Buzzard",
        "Garfield",
        "Heathcliff",
        "Dagwood",
        "Blondie Bumstead",
        "Andy Capp",
    ],
    "Stop Motion / Claymation": [
        "Wallace",
        "Gromit",
        "Feathers McGraw",
        "Gumby",
        "Pokey",
        "Prickle",
        "Minga",
        "Rudolph",
        "Yukon Cornelius",
        "Frosty",
        "Heat Miser",
        "Snow Miser",
        "Jack Skellington",
        "Oogie Boogie",
    ],
    "Web Animation / Internet Classics": ["Salad Fingers", "Hubert Cumberdale", "Marjory Stewart-Baxter", "Charlie", "Carl Llama", "Paul Llama"],
    "Brand Mascots": [
        "Tony the Tiger",
        "Snap",
        "Crackle",
        "Pop",
        "Toucan Sam",
        "Lucky the Leprechaun",
        "Cap’n Crunch",
        "Count Chocula",
        "Franken Berry",
        "Boo Berry",
        "Chester Cheetah",
        "Ronald McDonald",
        "Hamburglar",
        "Pillsbury Doughboy",
        "Mr. Peanut",
    ],
    "Gremlins (Movie)": ["Gizmo", "Stripe"],
}


APPEARANCE_PATTERNS = [
    "Carries {third}'s signature accessory, wrapped in the color palette of {second}, and keeps the silhouette reminiscent of {first}.",
    "Sports {first}'s most iconic outfit, but it is remixed with the futuristic flair of {second} and the playful shapes of {third}.",
    "Combines {first}'s face shape with {second}'s posture while wearing an outfit inspired by {third}.",
    "Mixes the antennae, ears, or hair details from {third} onto the body type of {first}, finished with the footwear style of {second}.",
]

PERSONALITY_PATTERNS = [
    "Has {first}'s attitude, the sense of humor of {second}, and the heroic (or mischievous) drive of {third}.",
    "Balances {first}'s caution with {second}'s impulsiveness and {third}'s optimism.",
    "Speaks with {first}'s cadence, schemes like {second}, yet cares with the heart of {third}.",
    "Approaches problems with {first}'s curiosity, {second}'s sarcasm, and {third}'s loyalty to friends.",
]

SIGNATURE_PATTERNS = [
    "Signature move: a combo attack that merges {first}'s trademark trick, {second}'s gadgetry or magic, and {third}'s speed.",
    "Ultimate gag: {first}-style slapstick timed with {second}'s dramatic flair and punctuated by a {third}-worthy catchphrase.",
    "Special skill: shapeshifts between silhouettes inspired by {first}, {second}, and {third}, keeping enemies guessing.",
    "Team role: the planner from {first}'s world, the wildcard energy of {second}, and the morale booster spirit of {third}.",
]


@dataclass(frozen=True)
class Inspiration:
    name: str
    franchise: str

    def full_label(self) -> str:
        return f"{self.name} ({self.franchise})"


@dataclass
class MashupCharacter:
    inspirations: Sequence[Inspiration]
    name: str
    appearance: str
    personality: str
    signature: str

    def render(self) -> str:
        inspiration_list = ", ".join(i.full_label() for i in self.inspirations)
        return (
            f"New Character: {self.name}\n"
            f"Inspirations: {inspiration_list}\n"
            f"Appearance: {self.appearance}\n"
            f"Personality: {self.personality}\n"
            f"Signature: {self.signature}\n"
        )


def flatten_pools(pools: dict[str, List[str]]) -> List[Inspiration]:
    """Convert the categorized pool into a flat list of Inspiration objects."""
    flattened: List[Inspiration] = []
    for franchise, characters in pools.items():
        flattened.extend(Inspiration(name=character, franchise=franchise) for character in characters)
    return flattened


def chunk_name_portmanteau(inspirations: Sequence[Inspiration]) -> str:
    """Create a playful blended name from the selected inspirations."""
    parts = []
    for inspiration in inspirations:
        first_word = inspiration.name.split()[0]
        take = max(2, min(4, len(first_word) // 2))
        parts.append(first_word[:take])
    return "".join(parts)


def choose_template(templates: Sequence[str], rng: random.Random) -> str:
    return rng.choice(list(templates))


def fill_template(template: str, inspirations: Sequence[Inspiration]) -> str:
    first, second, third = (i.name for i in inspirations)
    return template.format(first=first, second=second, third=third)


def generate_mashup(rng: random.Random, pool: Sequence[Inspiration]) -> MashupCharacter:
    inspirations = rng.sample(list(pool), 3)
    name = chunk_name_portmanteau(inspirations)
    appearance = fill_template(choose_template(APPEARANCE_PATTERNS, rng), inspirations)
    personality = fill_template(choose_template(PERSONALITY_PATTERNS, rng), inspirations)
    signature = fill_template(choose_template(SIGNATURE_PATTERNS, rng), inspirations)
    return MashupCharacter(
        inspirations=inspirations,
        name=name,
        appearance=appearance,
        personality=personality,
        signature=signature,
    )


def generate_multiple(count: int, seed: int | None = None) -> Iterable[MashupCharacter]:
    rng = random.Random(seed)
    pool = flatten_pools(CHARACTER_POOLS)
    for _ in range(count):
        yield generate_mashup(rng, pool)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate a blended cartoon character.")
    parser.add_argument("-n", "--count", type=int, default=1, help="Number of mashups to generate (default: 1).")
    parser.add_argument("--seed", type=int, help="Seed for deterministic output.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    mashups = list(generate_multiple(count=args.count, seed=args.seed))
    divider = "\n" + ("-" * 72) + "\n"
    print(divider.join(m.render().strip() for m in mashups))


if __name__ == "__main__":
    main()
