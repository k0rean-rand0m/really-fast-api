CREATE OR REPLACE FUNCTION procedure_template(params JSONB) RETURNS void AS $$
DECLARE
    _id     int    := params ->> 'id';
    _name   text   := params ->> 'name';
BEGIN
    -- An example of WS notify from procedure
    perform pg_notify('alert', '{"type": "procedure_template_notify", "details": {"id": ' || _id || ', "name": ' || _name || ',}}');
END
$$
    LANGUAGE 'plpgsql';