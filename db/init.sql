-- Dijalankan otomatis saat volume database masih kosong (pertama kali).
CREATE EXTENSION IF NOT EXISTS postgis;

CREATE TABLE users (
    id            SERIAL PRIMARY KEY,
    nama          VARCHAR(100) NOT NULL,
    email         VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    created_at    TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE crime_incidents (
    id                SERIAL PRIMARY KEY,
    jenis             VARCHAR(50)  NOT NULL,
    tingkat_keparahan SMALLINT     NOT NULL CHECK (tingkat_keparahan BETWEEN 1 AND 5),
    tanggal           DATE         NOT NULL,
    lokasi            GEOMETRY(Point, 4326) NOT NULL,
    kecamatan         VARCHAR(100),
    judul             VARCHAR(255) NOT NULL,
    ringkasan         TEXT,
    sumber_nama       VARCHAR(100),
    sumber_url        TEXT
);
CREATE INDEX idx_incidents_lokasi ON crime_incidents USING GIST (lokasi);

CREATE TABLE search_history (
    id         SERIAL PRIMARY KEY,
    user_id    INT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    keyword    VARCHAR(255) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE favorite_places (
    id      SERIAL PRIMARY KEY,
    user_id INT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    label   VARCHAR(50) NOT NULL,
    lokasi  GEOMETRY(Point, 4326) NOT NULL
);

CREATE TABLE user_settings (
    user_id   INT PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE,
    radius_km SMALLINT NOT NULL DEFAULT 3 CHECK (radius_km IN (1, 3, 5))
);

-- DATA CONTOH (dummy) hanya untuk menguji. Ganti dengan data berita asli.
-- Urutan ST_MakePoint: (longitude, latitude)
INSERT INTO crime_incidents (jenis, tingkat_keparahan, tanggal, lokasi, kecamatan, judul, ringkasan, sumber_nama, sumber_url) VALUES
('pencurian',    2, '2026-10-01', ST_SetSRID(ST_MakePoint(107.6989, -6.9535), 4326), 'Gedebage',    '[CONTOH] Pencurian sepeda motor', 'Data contoh untuk pengujian.', 'Contoh', 'https://example.com/1'),
('penjambretan', 3, '2026-10-10', ST_SetSRID(ST_MakePoint(107.7055, -6.9150), 4326), 'Ujungberung', '[CONTOH] Penjambretan di jalan',  'Data contoh untuk pengujian.', 'Contoh', 'https://example.com/2'),
('kekerasan',    5, '2026-10-20', ST_SetSRID(ST_MakePoint(107.7280, -6.9296), 4326), 'Cibiru',      '[CONTOH] Kasus kekerasan',        'Data contoh untuk pengujian.', 'Contoh', 'https://example.com/3');
