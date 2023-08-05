CREATE TABLE playlists (
    id INTEGER PRIMARY KEY,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE items (
    id INTEGER PRIMARY KEY,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,

    artist VARCHAR,
    duration INTEGER,
    played BOOLEAN DEFAULT FALSE,
    title VARCHAR,
    url VARCHAR,
    user_id VARCHAR NOT NULL,
    playlist_id INTEGER NOT NULL,
    FOREIGN KEY (playlist_id)
        REFERENCES playlists (id)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);
CREATE INDEX items_user_id_idx ON items (user_id);
CREATE INDEX items_playlist_id_idx ON items (playlist_id);
CREATE UNIQUE INDEX items_playlist_id_url_idx ON items (playlist_id, url) WHERE played IS FALSE;