const fs = require('fs');
const vm = require('vm');

const html = fs.readFileSync('index.html', 'utf8');
const scriptMatch = html.match(/<script>([\s\S]*)<\/script>/);
if (!scriptMatch) {
  console.error('Unable to locate embedded script block in index.html');
  process.exit(1);
}

function createStubElement() {
  return {
    addEventListener: () => {},
    set textContent(_) {},
    get textContent() {
      return '';
    },
    appendChild: () => {},
    innerHTML: '',
    value: '',
    checked: false,
    disabled: false,
    className: '',
    setAttribute: () => {},
    removeAttribute: () => {},
    style: {},
    click: () => {}
  };
}

const sandbox = {
  console,
  setTimeout,
  clearTimeout,
  document: {
    getElementById: () => createStubElement(),
    createElement: () => createStubElement()
  },
  navigator: {
    clipboard: {
      writeText: async () => {}
    }
  },
  alert: () => {},
  window: {},
  Blob: function (content, options) {
    this.content = content;
    this.options = options;
  },
  URL: {
    createObjectURL: () => 'blob:stub',
    revokeObjectURL: () => {}
  }
};

vm.createContext(sandbox);
vm.runInContext(scriptMatch[1], sandbox);

const tests = [];

function test(name, fn) {
  tests.push({ name, fn });
}

function assert(condition, message) {
  if (!condition) {
    throw new Error(message);
  }
}

test('createRiddleSet returns three variants with reasoning', () => {
  const result = sandbox.createRiddleSet({
    answer: 'lantern',
    hint: '',
    difficulty: 'Standard',
    useEmojis: true,
    useSymbols: true,
    includeAcrostic: false,
    includeHomophones: true,
    includeNumeric: true,
    includeDirectional: true,
    includeSensory: true
  });
  assert(result.variants.length >= 3, 'Expected at least three variants');
  result.variants.forEach((variant) => {
    assert(typeof variant.reasoning === 'string' && variant.reasoning.length > 0, 'Variant missing reasoning');
    assert(/Rule:/i.test(variant.text), 'Variant missing explicit rule line');
    assert(Array.isArray(variant.trap_tags) && variant.trap_tags.length >= 1, 'Variant missing trap tags');
  });
});

test('emoji variant fallback activates when emojis disabled', () => {
  const result = sandbox.createRiddleSet({
    answer: 'puzzle',
    hint: '',
    difficulty: 'Easy',
    useEmojis: false,
    useSymbols: true,
    includeAcrostic: false,
    includeHomophones: false,
    includeNumeric: false,
    includeDirectional: false,
    includeSensory: false
  });
  const secondVariant = result.variants[1];
  assert(secondVariant.title.includes('Classic'), 'Expected alternate classic when emojis disabled');
  assert(/consonants/.test(secondVariant.text), 'Fallback classic should mention consonants rule');
});

test('acrostic metadata matches canonical answer when enabled', () => {
  const result = sandbox.createRiddleSet({
    answer: 'forge',
    hint: 'Shape it hot',
    difficulty: 'Hard',
    useEmojis: true,
    useSymbols: true,
    includeAcrostic: true,
    includeHomophones: false,
    includeNumeric: true,
    includeDirectional: true,
    includeSensory: true
  });
  const symbolic = result.variants.find((variant) => variant.title === 'Symbolic/Spatial');
  assert(symbolic.metadata && symbolic.metadata.acrostic, 'Symbolic variant missing acrostic metadata');
  assert(symbolic.metadata.acrostic === 'FORGE', 'Acrostic metadata must match canonical answer');
});

test('variants enumerate acceptable answer spellings', () => {
  const result = sandbox.createRiddleSet({
    answer: 'cipher',
    hint: '',
    difficulty: 'Standard',
    useEmojis: true,
    useSymbols: true,
    includeAcrostic: false,
    includeHomophones: true,
    includeNumeric: false,
    includeDirectional: false,
    includeSensory: true
  });
  result.variants.forEach((variant) => {
    assert(Array.isArray(variant.acceptable_variants) && variant.acceptable_variants.length >= 1, 'Variant missing acceptable variants list');
    const normalized = variant.acceptable_variants.map((entry) => entry.toLowerCase());
    assert(normalized.includes('cipher'), 'Acceptable variants must contain the canonical answer');
  });
});

test('sensory variant meets line and trap requirements when enabled', () => {
  const result = sandbox.createRiddleSet({
    answer: 'blanket',
    hint: '',
    difficulty: 'Standard',
    useEmojis: true,
    useSymbols: true,
    includeAcrostic: false,
    includeHomophones: false,
    includeNumeric: false,
    includeDirectional: false,
    includeSensory: true
  });
  const sensory = result.variants.find((variant) => variant.title === 'Sensory Misdirect');
  assert(sensory, 'Expected sensory variant to be present');
  const lineCount = sensory.text.split('\n').length;
  assert(lineCount >= 2 && lineCount <= 4, 'Sensory variant must have between two and four lines');
  assert(sensory.trap_tags.includes('sensory-misdirect'), 'Sensory variant should include sensory trap tag');
  assert(/(smell|touch|feel|warm|heat|brush)/i.test(sensory.text), 'Sensory variant should reference a tactile or sensory cue');
});

let failed = 0;
for (const { name, fn } of tests) {
  try {
    fn();
    console.log(`✔ ${name}`);
  } catch (err) {
    failed++;
    console.error(`✖ ${name}: ${err.message}`);
  }
}

if (failed > 0) {
  process.exit(1);
} else {
  console.log(`All ${tests.length} tests passed.`);
}
