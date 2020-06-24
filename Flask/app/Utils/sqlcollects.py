
#查询接口列表
apis='''
        SELECT
            a.id,
            a.interface_name,
            p.project_name,
            a.interface_url,
            a.method,
            a.create_time,
            a.update_time
        FROM
            interfaces a
            LEFT JOIN Project p ON a.belong_project = p.id
'''

#通过项目查询接口
apiByprosql='''
SELECT
	s.interface_name
FROM
	interfaces s
WHERE
	s.belong_project IN (
	SELECT
		id
	FROM
		Project p
	WHERE
	p.project_name = "{}"
	)
'''

#通过用例ID查找步骤 api
reqinfosql='''

SELECT
    s.id,
	i.interface_url,
	i.interface_body,
	i.interface_param,
	i.method,
	s.assertion,
	s.assertresult,
	s.result,
	c.ispass,
	i.interface_header
FROM
	case_steps s
	LEFT JOIN interfaces i ON s.api_id = i.id
	left JOIN cases c ON c.id=s.case_id
WHERE
	s.case_id = "{}"

'''

if __name__ == '__main__':
    print(apiByprosql.format(""))