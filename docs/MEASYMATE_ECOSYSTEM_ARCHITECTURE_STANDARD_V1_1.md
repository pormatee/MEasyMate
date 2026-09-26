# MEasyMate Ecosystem Architecture Standard V1.1

**Document Type:** Ecosystem Architecture Standard / Shared Intelligence Layer  
**Version:** V1.1  
**Date:** 2026-09-26  
**Status:** APPROVED STANDARD EXTENSION  
**Owner:** MEasyMate  
**Extends:** `MEASYMATE_ECOSYSTEM_ARCHITECTURE_STANDARD_V1.md`

## 1. Purpose

เพิ่มมาตรฐาน Shared Intelligence Layer ให้ MEasyMate ใช้ความสามารถกลางร่วมกันข้าม Project โดยยังคงหลักว่าแต่ละ Domain Core เป็นเจ้าของ Business Decision ของตัวเอง

เป้าหมาย:

> **MEasyMate ต้องสามารถ “เห็น → เข้าใจ → เข้าใจสถานการณ์ → ตัดสินตาม Domain → ลงมือทำ” โดยใช้ Core กลางซ้ำได้หลาย Project**

## 2. Shared Intelligence Stack

```text
USER / REAL WORLD
      │
 ┌────┴────┐
 ▼         ▼
MEI       CBI
เห็น      เข้าใจการสื่อสาร
 └────┬────┘
      ▼
     MCI
เข้าใจสถานการณ์รวม
      ▼
 Domain Core
ตัดสินตามกติกางาน
      ▼
AI Hub (เมื่อจำเป็น)
      ▼
     MAI
   ลงมือทำ
```

## 3. MEI — MEasyMate Eye Intelligence

**บทบาท:** “ตาของ MEasyMate”

รับ Camera / Photo / Screenshot / Scan / PDF image / Form / Table / Factory image / Homework และแปลงเป็น Visual Object ที่ตรวจสอบย้อนกลับได้

Core flow:

```text
Capture
→ Normalize / Rotate / Crop / Deskew
→ Document / Scene Detection
→ Region / Column / Table / Geometry
→ Spatial OCR / Visual Token
→ Reading Order / Relation
→ Structure Reconstruction
→ Visual Object + Evidence + Confidence
```

MEI output ควรมีอย่างน้อย:

```text
source_id
document_id
region_id
geometry / bbox
object_type
text / value
relations
evidence
confidence
engine
contract_version
```

MEI ทำหน้าที่ “เห็นและเสนอความหมายจากภาพ” แต่ **ห้ามสรุป Root Cause, อนุมัติ Report, เปลี่ยน Business State หรือแทน Domain Core**

### HUE Relationship

HUE เป็น **Domain Adapter / First Field Domain ของ MEI**

```text
MEI Core
→ HUE Adapter
→ Homework Question / Choice / Math Layout / Problem Set
→ Learning Core
```

MEI Core ต้องไม่ผูกกับการบ้านเพียง Domain เดียว

## 4. CBI — Conversation Brain Intelligence

**บทบาท:** “เข้าใจสิ่งที่ผู้ใช้กำลังสื่อ”

รับผิดชอบ Intent, Entity, Reference, Topic, Context Change, Conversation State Interpretation, Confidence, Clarification และ Correction

```text
User Language
→ CBI
→ Semantic Meaning + Reference + Confidence
→ MCI / Domain Core
```

CBI ไม่ทำ Business Decision แทน Domain Core

## 5. MCI — MEasyMate Context Intelligence

**บทบาท:** “สมองกลางที่เข้าใจสถานการณ์รวม”

MCI รวม:

```text
MEI Visual Context
+ CBI Conversation Meaning
+ Project State
+ Session / Case State
+ User Reference
+ Evidence
+ Allowed History
+ Confidence / Uncertainty
= Situation Model
```

MCI Core Capabilities:

- Context Fusion
- Reference Resolution เช่น “ตรงนี้”, “รูปเมื่อกี้”, “ข้อด้านขวา”
- Situation Model
- Evidence Graph
- Confidence Fusion
- Clarification Policy
- Capability Routing
- AI Escalation Context
- Context Guard ป้องกันข้อมูลปนข้าม Project / Session / Case

MCI **ไม่ใช่ Business Brain** และห้ามตัดสิน Root Cause, Approval, Learning Result หรือ State Transition แทน Domain Core

## 6. Domain Core

Domain Core เป็น Authority ของกฎเฉพาะงาน เช่น:

- Learning Core
- Intelligence Coach Core
- Report Pro Core
- AI Hunter Core
- LocalLife Brain
- Factory Core
- Production Analytics Core

Domain Core เป็นเจ้าของ Business Rule, Gate, State Transition, Approval, Validation Policy และ Source-of-Truth adoption

## 7. MEasyMate AI Hub

มาตรฐาน:

```text
LOCAL FIRST
→ Shared Intelligence / Domain Core
→ confidence ไม่พอหรือ Policy อนุญาต
→ AI Hub
→ AI Proposal
→ Validator / MCI / Domain Core
→ Accept / Clarify / Reject
```

External AI:
- ไม่เป็น Source of Truth โดยอัตโนมัติ
- ไม่เปลี่ยน Business State โดยตรง
- ไม่เขียน Production Canonical Data โดยตรง
- ต้องผ่าน Provider-neutral contract / Entitlement / Quota / Cost / Privacy policy

## 8. MAI — MEasyMate Action Intelligence

**บทบาท:** “มือของ MEasyMate”

แปลง Approved Intent / Approved Domain Action เป็นการลงมือทำ เช่น:

- สร้างหรือกรอก Report
- Update Form
- สร้างไฟล์
- ส่งข้อมูล
- เรียก Tool / Connector
- Trigger Workflow
- Execute approved local action

Flow:

```text
MCI understands situation
→ Domain Core decides
→ Action Contract
→ MAI validates / executes
→ Tool / Connector / App
→ Result + Evidence + Trace
```

MAI ห้ามสร้าง Business Decision ใหม่เอง และต้องตรวจ permission / entitlement / confirmation / trace

## 9. Common Intelligence Contract

Shared Intelligence ควรรองรับ:

```text
project_id
domain_id
session_id
case_id
request_id
source_id
state_version
capability
contract_version
timestamp
```

เมื่อเกี่ยวข้อง:

```text
document_id
region_id
turn
user_reference
evidence_refs[]
confidence
uncertainty
source_engine
proposal_status
trace_id
```

หลักสำคัญ:

> **ทุก Fact / Proposal ต้องบอกได้ว่า “มาจากไหน”, “เชื่อมั่นแค่ไหน”, “อยู่ใน Case ไหน”**

## 10. Intelligence Object Status

```text
OBSERVED
EXTRACTED
INFERRED
PROPOSED
USER_CONFIRMED
DOMAIN_VERIFIED
REJECTED
UNKNOWN
```

Engine ห้ามทำ `PROPOSED → DOMAIN_VERIFIED` เอง เว้นแต่ Domain Contract อนุญาตผ่าน Deterministic Validator

## 11. Context Isolation Standard

ต้องกันข้อมูลปนระหว่าง:

```text
Project
Domain
Session
Case
Document
Hunt
Report
Learning Problem
Factory Incident
```

Default:

> **No implicit cross-case merge**

การ reuse context ข้าม Case ต้องมี explicit reference / policy / user action

## 12. Current Project Adoption Map

- **Learning Platform:** MEI → HUE Adapter, CBI → learner conversation, MCI → current problem/image/question context
- **Intelligence Coach:** MEI → defect/WI/checklist evidence, CBI → problem-solving conversation, MCI → evidence + current step + case context
- **Report Pro:** MEI → image/document evidence, CBI → report intent, MCI → event/5W2H context
- **AI Hunter:** MEI → screenshot/document evidence, CBI → hunt commands, MCI → Hunt Context / evidence isolation / signal relation
- **Factory Forms:** MEI → form/table/checkbox, CBI → user input, MCI → shift/group/form/incident context
- **Production Dashboard:** CBI → analytical question, MCI → line/shift/time/metric/incident context
- **LocalLife:** CBI → request meaning, MCI → place/reference/current context
- **AI Guide:** CBI → goal, MCI → work-item context/missing info/prior artifact
- **Secretary System:** CBI → secretary command, MCI → project/version/decision/blocker/next-work context

## 13. New Shared Intelligence Gate

ก่อนสร้าง Engine / Capability ใหม่ ต้องตอบ:

```text
[ ] เป็น Perception, Conversation, Context, Domain Decision หรือ Action?
[ ] ควรอยู่ MEI / CBI / MCI / Domain Core / MAI หรือไม่?
[ ] Source / Evidence อยู่ที่ใด?
[ ] Confidence / Uncertainty ถูกเก็บหรือไม่?
[ ] Context Isolation ใช้ key อะไร?
[ ] ใครเป็น Authority?
[ ] AI เป็น Proposal หรือ Decision?
[ ] Offline / Local-first path มีหรือไม่?
[ ] Contract Version คืออะไร?
[ ] Failure แล้ว Fail-safe / Fail-closed อย่างไร?
[ ] Reuse ข้าม Project ได้โดยไม่ผูก Domain หรือไม่?
```

## 14. Permanent Architecture Principles

1. **MEI = เห็น**
2. **CBI = เข้าใจการสื่อสาร**
3. **MCI = เข้าใจสถานการณ์รวม**
4. **Domain Core = ตัดสินตามกติกางาน**
5. **AI Hub = เรียก External AI เมื่อจำเป็น**
6. **MAI = ลงมือทำตาม Action ที่ได้รับอนุมัติ**
7. Shared Intelligence ไม่แทน Domain Authority
8. Local-first เป็น Default เมื่อ Product Architecture รองรับ
9. AI output เป็น Proposal จนกว่าจะผ่าน Validation/Confirmation
10. ทุก Intelligence Object ต้องมี Source / Evidence / Confidence / Context
11. ห้าม Context ปนข้าม Case โดย implicit merge
12. Shared Core ต้อง reuse ได้หลาย Project ผ่าน Adapter / Contract
13. Domain Knowledge อยู่ Domain Pack / Adapter ไม่ฝังใน Shared Core โดยไม่จำเป็น
14. Business State เปลี่ยนโดย Domain Authority หรือ Explicit User Action เท่านั้น
15. ระบบต้องย้อนรอยได้ว่า **เห็นอะไร → เข้าใจอะไร → เชื่อมอย่างไร → ใครตัดสิน → ทำอะไร**

## 15. Final Principle

> **MEasyMate ไม่สร้าง Super Brain ตัวเดียวที่ทำทุกอย่าง แต่สร้าง Intelligence หลายชั้นที่รับผิดชอบชัดเจน: MEI เห็น, CBI เข้าใจการสื่อสาร, MCI เข้าใจสถานการณ์, Domain Core ตัดสิน, AI Hub ช่วยเมื่อจำเป็น และ MAI ลงมือทำ — ทุกชั้นเชื่อมกันด้วย Evidence, Confidence, Context และ Versioned Contract**

**Compatibility:** V1.1 ขยาย V1 และไม่ยกเลิก Domain-owned Source of Truth, Project Brain ownership, AI Hub boundary, Bridge/SDK, Entitlement หรือ Fail-Closed Contract rules ของ V1
