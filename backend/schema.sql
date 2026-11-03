-- Created automatically when the server starts (CREATE TABLE IF NOT EXISTS); safe to run again.
-- Times are milliseconds since 1970 (UTC), except payment_time, which is Razorpay's seconds.

CREATE TABLE IF NOT EXISTS bookings (
  id                   VARCHAR(40)  NOT NULL PRIMARY KEY,   -- our booking id, also Razorpay's reference_id
  event_slug           VARCHAR(64)  NOT NULL,
  quantity             SMALLINT UNSIGNED NOT NULL,
  unit_price_paise     INT UNSIGNED NOT NULL,
  amount_paise         INT UNSIGNED NOT NULL,
  currency             CHAR(3)      NOT NULL DEFAULT 'INR',
  status               VARCHAR(16)  NOT NULL,                -- created | paid | review | expired | cancelled | failed
  payment_link_id      VARCHAR(64)  NULL UNIQUE,
  payment_link_url     VARCHAR(255) NULL,
  payment_id           VARCHAR(64)  NULL UNIQUE,
  consent              TINYINT(1)   NOT NULL DEFAULT 0,      -- guest agreed to share identifiers with Meta
  fbp                  VARCHAR(255) NULL,                    -- identifiers are kept only with consent,
  fbc                  VARCHAR(512) NULL,                    -- and cleared once Meta has the event
  client_ip            VARCHAR(64)  NULL,
  user_agent           VARCHAR(512) NULL,
  em_hash              CHAR(64)     NULL,                    -- SHA-256 of the normalised email, never the email
  ph_hash              CHAR(64)     NULL,                    -- SHA-256 of the normalised phone, never the phone
  created_at           BIGINT       NOT NULL,
  expires_at           BIGINT       NOT NULL,
  paid_at              BIGINT       NULL,
  payment_time         BIGINT       NULL,
  meta_status          VARCHAR(16)  NOT NULL DEFAULT 'pending', -- pending | sending | sent | failed | skipped | expired | abandoned
  meta_attempts        INT          NOT NULL DEFAULT 0,
  meta_last_attempt_at BIGINT       NULL,
  meta_last_error      VARCHAR(500) NULL,
  meta_fbtrace_id      VARCHAR(64)  NULL,
  KEY bookings_status (event_slug, status),
  KEY bookings_meta (status, meta_status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS webhook_events (
  event_id     VARCHAR(64) NOT NULL PRIMARY KEY,             -- Razorpay's X-Razorpay-Event-Id
  event        VARCHAR(64) NOT NULL,
  received_at  BIGINT      NOT NULL,
  result       VARCHAR(32) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
