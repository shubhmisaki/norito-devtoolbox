(function (root) {
  const WORDLIST = [
    "acorn","action","adobe","agile","alert","alpha","amber","anchor","angle","apple",
    "arena","armor","arrow","artist","aspen","atlas","aurora","autumn","avenue","azure",
    "badge","bakery","balloon","bamboo","banjo","basil","beacon","berry","bicycle","birch",
    "blanket","blaze","blossom","boulder","breeze","bridge","bronze","bubble","cabin","camel",
    "canary","candle","canyon","captain","caramel","carbon","cargo","carrot","cascade","cedar",
    "ceramic","cherry","chess","chimney","cinder","citrus","clover","cobalt","comet","compass",
    "coral","cotton","coyote","crane","crater","cricket","crimson","crystal","cuddle","cypress",
    "dagger","daisy","dandelion","delta","denim","desert","diamond","dolphin","domino","dragon",
    "drift","drizzle","dune","eagle","ebony","echo","eclipse","elbow","elder","ember",
    "emerald","engine","ensign","falcon","feather","fennel","ferry","fiber","fiddle","filament",
    "flame","flannel","flare","flint","forest","forge","fossil","foxglove","frost","galaxy",
    "garnet","gazelle","gecko","ginger","glacier","gorge","granite","grape","gravel","guitar",
    "gully","harbor","harvest","hazel","heather","hemlock","heron","hickory","honey","horizon",
    "hummingbird","hyacinth","ibis","icicle","indigo","ink","inlet","ivory","jade","jaguar",
    "jasmine","jasper","jelly","jetty","jigsaw","journey","jungle","juniper","karma","kayak",
    "kestrel","kettle","kiln","kingfisher","kiwi","koala","lagoon","lantern","larch","lavender",
    "lemur","lentil","lichen","lilac","lily","linen","lively","lizard","locket","lotus",
    "lumber","lupine","lynx","magma","magnet","magpie","mahogany","mallow","mandarin","mangrove",
    "maple","marble","marigold","marsh","meadow","mercury","meridian","meteor","mimosa","mint",
    "mirage","mirth","mistral","moccasin","mosaic","mountain","mulberry","mushroom","myrtle","nautilus",
    "nebula","nectar","needle","nettle","newt","nickel","nimbus","noble","nomad","nutmeg",
    "oasis","oatmeal","obsidian","ocean","ocelot","olive","onyx","opal","orange","orbit",
    "orca","orchard","orchid","oregano","origami","osprey","otter","outpost","owl","oxide",
    "paisley","palette","panda","panther","papaya","paprika","parchment","parsley","pasture","pebble",
    "pecan","pelican","pepper","periwinkle","petal","pheasant","pigeon","pilot","pine","pinnacle",
    "pioneer","pistachio","planet","plaza","plum","pomegranate","poplar","poppy","porcelain","prairie",
    "prism","puffin","pumice","quail","quarry","quartz","quill","quilt","quince","rabbit",
    "raccoon","radish","rainbow","raven","redwood","reef","reindeer","ribbon","ridge","ripple",
    "river","robin","rocket","rosemary","rowan","ruby","saddle","saffron","sage","sailor",
    "salamander","salmon","sandpiper","sapphire","satchel","savanna","scarab","sequoia","shadow","shale",
    "shamrock","shell","shore","silver","siskin","skylark","slate","sleet","sloth","snapdragon",
    "snowfall","sorrel","sparrow","spearmint","sphinx","spice","spiral","spruce","squid","starling",
    "storm","sugar","summit","sundew","sunflower","sunrise","swallow","sycamore","tangerine","tapestry",
    "tarragon","tawny","temple","terrace","thicket","thistle","thunder","thyme","tiger","timber",
    "topaz","tortoise","toucan","trellis","trout","tulip","tumbleweed","tundra","tunnel","turmeric",
    "turquoise","turtle","umber","umbrella","unicorn","urchin","valley","vanilla","velvet","verbena",
    "vessel","vine","violet","viper","vista","voyage","walnut","walrus","wander","warbler",
    "waterfall","wattle","wave","weasel","whisker","whistle","wicker","widget","willow","wisteria",
    "wolverine","wombat","woodland","wren","xenon","yarrow","yew","zephyr","zinnia","zircon",
  ];

  const unique = Array.from(new Set(WORDLIST));

  const api = { WORDLIST: unique };
  if (typeof module !== "undefined" && module.exports) module.exports = api;
  else Object.assign(root, api);
})(typeof window !== "undefined" ? window : globalThis);
