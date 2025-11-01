export interface ChecklistItem {
  id: string;
  label: string;
  required: boolean;
  description?: string;
}

export interface ChecklistTemplate {
  id: string;
  locale: string;
  category: string;
  title: string;
  items: ChecklistItem[];
}

export interface ChecklistTemplatesResponse {
  templates: ChecklistTemplate[];
}

export type ChecklistMapEntry = Record<string, string | boolean | null>;

export interface ChecklistResponseV2 {
  items: ChecklistMapEntry[];
}

export interface ChecklistCheck {
  item_id: string;
  checked: boolean;
  memo?: string;
}

export interface SaveChecklistPayload {
  checks: ChecklistCheck[];
}

export interface RoomPhoto {
  photo_id: string;
  object_url: string;
  created_at: string;
}

export interface Room {
  room_id: string;
  address: string;
  type: string;
  floor: number;
  deposit: number;
  rent_monthly: number;
  fee_included: boolean;
  fee_mgmt?: number;
  created_at: string;
  photos: RoomPhoto[];
  checklist?: RoomChecklist;
}

export interface CreateRoomPayload {
  address: string;
  type: string;
  floor: number;
  deposit: number;
  rent_monthly: number;
  fee_included: boolean;
  fee_mgmt?: number;
  checklist: RoomChecklist;
}

export interface RoomChecklist {
  items: ChecklistMapEntry[];
}

export interface OcrUploadResponse {
  ocr_id: string;
  object_url: string;
}

export type OcrStage = 'queued' | 'processing' | 'done' | 'failed';

export interface OcrField {
  key: string;
  value: string;
  confidence?: number;
}

export interface OcrReport {
  ocr_id: string;
  status: OcrStage;
  text: string;
  fields?: OcrField[];
  created_at: string;
}

export type LlmStage = 'queued' | 'processing' | 'done' | 'failed';

export interface LlmReport {
  room_id: string;
  user_id: string;
  status: LlmStage;
  summary?: string;
  highlights?: string[];
  recommendations?: string[];
  created_at: string;
}

export interface SttBubble {
  id: string;
  speaker: number | null;
  text: string;
  started_at?: number;
  ended_at?: number;
}
