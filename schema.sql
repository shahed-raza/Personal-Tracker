CREATE TABLE "logs" (
    "id" INTEGER,
    "logged_at" DATETIME DEFAULT CURRENT_TIMESTAMP,
    "title" TEXT NOT NULL,
    -- programatically ensure progress tracking, enligtening, though provoking and something which i personally struggle with is being asked and entered
    -- like, how this task went, distractions, problems, etc (Keep it simple)
    "content" TEXT,
    "distractions" TEXT, -- though null is accepted (cause rarely no distractins might be logged), but be sure to clearly ask in the front-end
    "problems" TEXT, -- though null is accepted (cause rarely no problems might be logged), but be sure to clearly ask in the front-end
    "start_time" TEXT, -- optional
    "end_time" TEXT, -- optional
    "time_taken_hours" NUMERIC, -- optional
    "time_takn_minutes" NUMERIC, -- optional
    PRIMARY KEY("id")
);

-- keep the to_do as simple as possible, kinda like "Grit App"
CREATE TABLE "todos" (
    "id" INTEGER,
    "created_at" DATETIME DEFAULT CURRENT_TIMESTAMP, -- enforce no changes after 1st insertion using triggers
    "modified_at" DATETIME DEFAULT CURRENT_TIMESTAMP,
    "title" TEXT NOT NULL,
    -- programatically ensure todo_data is entered such that i precisely provides clarity on how a to-do should be for me
    -- tailored according to me
    "content" TEXT, --optional
    "priority" INTEGER CHECK("priority" IN (1, 2, 3, 4)), -- lower no. ==> higher priority -- optional
    "reminder" DATETIME, -- optional
    "estimated_hours" NUMERIC, -- optional
    "estimated_minutes" NUMERIC, -- optional
    PRIMARY KEY("id")
);

CREATE TABLE "notes" (
    "id" INTEGER,
    "created_at" DATETIME DEFAULT CURRENT_TIMESTAMP, -- enforce no changes after 1st insertion using triggers
    "modified_at" DATETIME DEFAULT CURRENT_TIMESTAMP,
    "title" TEXT NOT NULL,
    -- programatically ensure the data entered is with precisely entered helping me gain clarity
    "content" TEXT,
    "tag" TEXT,
    PRIMARY KEY("id")
);

CREATE TRIGGER "prevent_created_at_update_notes"
BEFORE UPDATE OF "created_at" ON "notes"
FOR EACH ROW
BEGIN
    SELECT RAISE(ABORT, "created_at is immutable");
END;

CREATE TRIGGER "prevent_created_at_update_todos"
BEFORE UPDATE ON "created_at" ON "todos"
FOR EACH ROW
BEGIN
    SELECT RAISE(ABORT, "created_at is immutabe");
END;
