SELECT *
FROM pa004.users AS u
INNER JOIN pa004.vehicle AS v ON (u.id = v.id)
INNER JOIN pa004.insurance AS i ON (u.id = i.id)
ORDER BY u.id ASC
LIMIT 20;