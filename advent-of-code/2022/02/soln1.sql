with
    scores as (
        select
            case
                when self = opp then 3 -- draw

                -- win
                when opp = 'r' and self = 'p' then 6
                when opp = 'p' and self = 's' then 6
                when opp = 's' and self = 'r' then 6

                -- loss
                else 0
            end as gameresult_score,

            case
                when self = 'r' then 1
                when self = 'p' then 2
                else 3
            end as selection_score,
            *
        from strategy
    )
select sum(gameresult_score + selection_score) from scores
-- select * from scores limit 10
