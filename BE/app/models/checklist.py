from typing import List, Optional

from pydantic import BaseModel, Field


class ChecklistItem(BaseModel):
    key: str = Field(..., description="Unique key for the checklist entry.")
    label: str = Field(..., description="Display label shown to users.")
    description: Optional[str] = Field(
        default=None,
        description="Optional extra guidance for the item.",
    )


class ChecklistCategory(BaseModel):
    key: str = Field(..., description="Category identifier.")
    label: str = Field(..., description="Category display label.")
    items: List[ChecklistItem]


class ChecklistTemplate(BaseModel):
    checklist_id: str = Field(..., description="Template identifier.")
    title: str = Field(..., description="Human readable template title.")
    categories: List[ChecklistCategory]


class ChecklistListResponse(BaseModel):
    items: List[ChecklistTemplate]


DEFAULT_CHECKLIST_TEMPLATE = ChecklistTemplate(
    checklist_id="cl_lease_v1",
    title="임대차 체크리스트",
    categories=[
        ChecklistCategory(
            key="plumbing",
            label="수도와 배수",
            items=[
                ChecklistItem(key="water_flow_general", label="싱크대/세면대/샤워기 물은 잘 나오는가"),
                ChecklistItem(key="toilet_flush", label="변기 물은 잘 내려가는가"),
                ChecklistItem(key="hot_water", label="싱크대/화장실 온수는 잘 나오는가"),
            ],
        ),
        ChecklistCategory(
            key="windows",
            label="창문",
            items=[
                ChecklistItem(key="sunlight", label="햇빛은 잘 들어오는가"),
                ChecklistItem(key="window_safety", label="방충망/방범창은 이상 없는가"),
                ChecklistItem(key="privacy", label="옆 건물에서 너무 잘 보이지 않는가"),
            ],
        ),
        ChecklistCategory(
            key="bathroom",
            label="화장실",
            items=[
                ChecklistItem(key="bathroom_window", label="화장실 내부에 창문이 있는가"),
                ChecklistItem(key="bathroom_smell", label="배수구 냄새는 나지 않는가"),
                ChecklistItem(key="bathroom_space", label="공간이 충분히 넓은가"),
            ],
        ),
        ChecklistCategory(
            key="neighborhood",
            label="주변 환경",
            items=[
                ChecklistItem(key="public_transport", label="대중교통 이용은 편리한가"),
                ChecklistItem(key="amenities", label="편의점, 은행 등 편의시설이 있는가"),
                ChecklistItem(key="hill", label="언덕에 있는가"),
            ],
        ),
        ChecklistCategory(
            key="details",
            label="디테일",
            items=[
                ChecklistItem(key="mold", label="벽지에 곰팡이 흔적은 없는가"),
                ChecklistItem(key="pest_control", label="바퀴약 설치는 없는가"),
                ChecklistItem(key="outlets", label="콘센트 개수는 충분한가"),
            ],
        ),
        ChecklistCategory(
            key="security",
            label="보안",
            items=[
                ChecklistItem(key="door_lock", label="공동현관 비밀번호가 있는가"),
                ChecklistItem(key="cctv", label="출입구와 복도에 CCTV가 있는가"),
                ChecklistItem(key="landlord_residence", label="건물에 집주인이 사는가"),
            ],
        ),
    ],
)
