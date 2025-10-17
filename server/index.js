// server/index.js
const express = require('express');
const fs = require('fs');
const path = require('path');

const app = express();
const PORT = 3001;

const rulesDirectory = path.join(__dirname, '../rules/sigma');

app.use(express.json());

app.get('/api/health', (req, res) => {
  res.status(200).json({ status: 'API is up and running' });
});

app.get('/api/rules', (req, res) => {
  try {
    const files = fs.readdirSync(rulesDirectory);
    const ruleFiles = files.filter(file => file.endsWith('.yml') || file.endsWith('.yaml'));
    res.status(200).json({ rules: ruleFiles });
  } catch (error) {
    console.error('Error reading rules directory:', error);
    res.status(500).json({ error: 'Failed to read rules directory' });
  }
});

app.get('/api/rules/:filename', (req, res) => {
  try {
    const { filename } = req.params;
    if (filename.includes('..')) {
      return res.status(400).json({ error: 'Invalid filename' });
    }
    const filePath = path.join(rulesDirectory, filename);
    if (!fs.existsSync(filePath)) {
      return res.status(404).json({ error: 'Rule not found' });
    }
    const fileContent = fs.readFileSync(filePath, 'utf8');
    res.setHeader('Content-Type', 'text/plain');
    res.status(200).send(fileContent);
  } catch (error) {
    console.error(`Error reading rule ${req.params.filename}:`, error);
    res.status(500).json({ error: 'Failed to read rule file' });
  }
});

// --- NEW ENDPOINT ---
// POST /api/rules - Creates a new rule file
app.post('/api/rules', (req, res) => {
    try {
        const { filename, content } = req.body;

        // Basic validation
        if (!filename || !content) {
            return res.status(400).json({ error: 'Filename and content are required' });
        }

        // Ensure filename is a .yml or .yaml file
        if (!filename.endsWith('.yml') && !filename.endsWith('.yaml')) {
            return res.status(400).json({ error: 'Filename must end with .yml or .yaml' });
        }

        const filePath = path.join(rulesDirectory, filename);

        // Check if file already exists
        if (fs.existsSync(filePath)) {
            return res.status(409).json({ error: 'A rule with this filename already exists' });
        }

        // Write the new file
        fs.writeFileSync(filePath, content, 'utf8');
        res.status(201).json({ message: `Rule '${filename}' created successfully` });

    } catch (error) {
        console.error('Error creating rule:', error);
        res.status(500).json({ error: 'Failed to create rule file' });
    }
});


app.listen(PORT, () => {
  console.log(`✅ Server is listening on http://localhost:${PORT}`);
});
