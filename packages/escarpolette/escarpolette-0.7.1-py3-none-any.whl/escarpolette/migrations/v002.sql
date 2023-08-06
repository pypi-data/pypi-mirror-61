ALTER TABLE items ADD COLUMN position INTEGER NOT NULL DEFAULT 0;

WITH positions AS (
    SELECT
        id,
        row_number() OVER (PARTITION BY playlist_id ORDER BY created_at) AS rn
    FROM items
)
UPDATE items SET position = (SELECT rn FROM positions WHERE id = items.id);


CREATE UNIQUE INDEX items_playlist_id_order_idx ON items (playlist_id, position);
