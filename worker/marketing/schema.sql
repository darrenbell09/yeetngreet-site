CREATE TABLE IF NOT EXISTS marketing_subscribers (
  email TEXT PRIMARY KEY COLLATE NOCASE,
  consented_at TEXT NOT NULL,
  source TEXT NOT NULL,
  source_path TEXT,
  consent_text TEXT NOT NULL,
  created_at TEXT NOT NULL DEFAULT (datetime('now')),
  unsubscribed_at TEXT
);
