import os,re,uuid
from .db import q
THRESH=int(os.getenv('REFUND_APPROVAL_THRESHOLD','10000'))
ID=re.compile(r'\b(?:CUS|ORD|TKT|EMP|SKU|REF)-[A-Z0-9-]+\b',re.I)
def ids(t): return [x.upper() for x in ID.findall(t)]
def result(answer,action,evidence,details=None,status='COMPLETED',confidence=.99):
 return {'status':status,'answer':answer,'action':action,'evidence':evidence,'confidence':confidence,'details':details or {}}
def employee(t):
 xs=[x for x in ids(t) if x.startswith('EMP-')]
 if not xs:return result('Please provide an employee ID.','Identified an employee lookup.',['employees'],status='CLARIFICATION_REQUIRED',confidence=.92)
 r=q('SELECT e.id,e.name,e.role,e.base_pay,e.active,p.performance,p.participation,p.shifts_completed,p.shifts_scheduled,p.production,p.production_target,p.skill_test,p.attendance,p.experience_years,p.skills,pr.status payroll_status,pr.net_pay FROM employees e LEFT JOIN employee_performance p ON p.employee_id=e.id LEFT JOIN payroll pr ON pr.employee_id=e.id WHERE e.id=%s',(xs[0],))
 if not r:return result(f'No employee found for {xs[0]}.',f'Searched employee {xs[0]}.',['employees'],confidence=.97)
 x=r[0];s=t.lower()
 if re.search(r'\b(name|who)\b',s) and not any(k in s for k in ['pay','salary','performance','role','promotion','bonus','shift']): return result(x['name'],f'Looked up employee {xs[0]}.',['employees'],{'employee':x})
 if any(k in s for k in ['paycheck','payroll','salary','pay status']): return result(str(x.get('payroll_status') or 'No payroll status recorded.'),f'Checked payroll for {xs[0]}.',['employees','payroll'],{'employee':x})
 if 'role' in s:return result(x['role'],f'Checked role for {xs[0]}.',['employees'],{'employee':x})
 return result(f"{x['name']} — {x['role']}",f'Looked up employee {xs[0]}.',['employees','employee_performance','payroll'],{'employee':x})
def customer(t):
 xs=[x for x in ids(t) if x.startswith('CUS-')]
 if not xs:return result('Please provide a customer ID.','Identified a customer lookup.',['customers'],status='CLARIFICATION_REQUIRED',confidence=.92)
 r=q('SELECT * FROM customers WHERE id=%s',(xs[0],))
 if not r:return result(f'No customer found for {xs[0]}.',f'Searched customer {xs[0]}.',['customers'],confidence=.97)
 x=r[0];s=t.lower()
 if 'discount' in s:return result('Eligible' if int(x.get('loyalty_score') or 0)>=50 else 'Not eligible',f'Checked discount eligibility for {xs[0]}.',['customers','discount policy'],{'customer':x})
 if re.search(r'\b(name|who)\b',s):return result(x['name'],f'Looked up customer {xs[0]}.',['customers'],{'customer':x})
 return result(x['name'],f'Looked up customer {xs[0]}.',['customers'],{'customer':x})
def inventory(t):
 rows=q('SELECT i.sku,i.product,i.stock,i.reorder_point,i.reorder_qty,i.vendor_id,i.unit_cost,v.name vendor_name,v.email vendor_email FROM inventory i LEFT JOIN vendors v ON v.id=i.vendor_id ORDER BY i.stock ASC')
 low=[r for r in rows if int(r.get('stock') or 0)<=int(r.get('reorder_point') or 0)]
 table=[{'SKU':r['sku'],'Item':r['product'],'Stock':r['stock'],'Reorder point':r['reorder_point'],'Reorder qty':r['reorder_qty'],'Vendor':r.get('vendor_name'),'Vendor email':r.get('vendor_email')} for r in low]
 names=', '.join(r['product'] for r in low)
 answer=f'{len(low)} low-stock item(s): {names}.' if low else 'No items are currently low in stock.'
 return result(answer,f'Checked {len(rows)} inventory items and compared stock against each reorder point.',['inventory','vendors'],{'count':len(low),'items':table})
def tickets(t):
 rows=q('SELECT * FROM tickets'); solved=[r for r in rows if r.get('auto_solved') or str(r.get('status','')).upper() in ('SOLVED','CLOSED','SOLVED_AUTOMATICALLY')];pending=[r for r in rows if r not in solved]
 return result(f'{len(solved)} ticket(s) solved and {len(pending)} pending.',f'Reviewed {len(rows)} customer tickets.',['tickets'],{'solved':solved,'pending':pending})
def refunds(t):
 xs=[x for x in ids(t) if x.startswith(('ORD-','CUS-','REF-'))];w='';p=[]
 if xs:
  w=' WHERE '+' OR '.join(('o.id=%s' if x.startswith('ORD-') else 'o.customer_id=%s' if x.startswith('CUS-') else 'r.id=%s') for x in xs);p=xs
 rows=q('SELECT o.id order_id,o.customer_id,o.amount,o.return_window_days,o.days_since_delivery,o.payment_status,o.refund_status FROM orders o LEFT JOIN refunds r ON r.order_id=o.id'+w,p)
 decisions=[]
 for r in rows:
  pay=str(r.get('payment_status') or '').upper();already=str(r.get('refund_status') or '').upper() in ('REFUNDED','COMPLETED')
  if pay!='PAID':st='REJECTED';reason='Payment was not completed.'
  elif already:st='REJECTED';reason='Refund has already been processed.'
  elif int(r['days_since_delivery'])>int(r['return_window_days']):st='REJECTED';reason=f"Return window expired: {r['days_since_delivery']} days exceeds the {r['return_window_days']}-day policy."
  elif float(r['amount'])>=THRESH:st='PENDING';reason=f"Eligible, but amount {r['amount']} meets/exceeds the {THRESH} approval threshold."
  else:st='APPROVED';reason='Eligible: payment completed, return window valid, and amount is below the approval threshold.'
  decisions.append({'Order':r['order_id'],'Amount':r['amount'],'Status':st,'Reason':reason})
 a=sum(x['Status']=='APPROVED' for x in decisions);pn=sum(x['Status']=='PENDING' for x in decisions);rej=sum(x['Status']=='REJECTED' for x in decisions)
 return result(f'{a} approved, {pn} pending human approval, {rej} rejected.',f'Reviewed refund policy, payment, return-window and prior-refund status for {len(rows)} order(s).',['orders','refunds','payment status','return policy'],{'approved':a,'pending':pn,'rejected':rej,'decisions':decisions},'HUMAN_APPROVAL_REQUIRED' if pn else 'COMPLETED')
def run(t):
 s=t.lower()
 if any(k in s for k in ['refund','return money']):return refunds(t)
 if any(k in s for k in ['low stock','inventory','stock','reorder','restock']):return inventory(t)
 if 'ticket' in s:return tickets(t)
 if any(k in s for k in ['employee','paycheck','payroll','salary','promotion','bonus','performance','shift']):return employee(t)
 if any(k in s for k in ['customer','discount']):return customer(t)
 return result('I need a supported business operation to execute this request.','Classified the request and checked supported operations.',['company data'],status='CLARIFICATION_REQUIRED',confidence=.90)
